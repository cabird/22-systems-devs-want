#!/usr/bin/env python3
"""Build a sanitized version of the survey report by replacing quotes with vetted ones."""

import json
import re
import sys
from pathlib import Path

ORIGINAL = Path("/home/cbird/rudy_survey_data_analysis_2026/academic_results/survey_analysis_report.html")
OUTPUT = Path("/home/cbird/22-systems-devs-want/report.html")
CATEGORIES = ["design_planning", "development", "quality_risk", "infrastructure_ops", "meta_work"]
VETTED_DIR = Path("/tmp")


def load_vetted_quotes():
    """Load all vetted quote files and merge into one dict."""
    merged = {}
    for cat in CATEGORIES:
        path = VETTED_DIR / f"vetted_{cat}.json"
        with open(path) as f:
            data = json.load(f)
        merged.update(data)
    return merged


def parse_modal_data(html):
    """Extract and parse the MODAL_DATA JavaScript object from the HTML."""
    m = re.search(r"var MODAL_DATA\s*=\s*\{", html)
    if not m:
        raise ValueError("MODAL_DATA not found in HTML")
    brace_start = html.index("{", m.start())
    depth = 0
    for i in range(brace_start, len(html)):
        if html[i] == "{":
            depth += 1
        elif html[i] == "}":
            depth -= 1
        if depth == 0:
            brace_end = i
            break
    json_str = html[brace_start : brace_end + 1]
    data = json.loads(json_str)
    return data, m.start(), brace_end + 1


def build_proj_theme_mapping(modal_data):
    """Map modal-proj-X-N-theme keys to their corresponding modal-codebook-X-Y keys."""
    mapping = {}
    for cat in CATEGORIES:
        proj_themes = [k for k in modal_data if k.startswith(f"modal-proj-{cat}-") and k.endswith("-theme")]
        codebook_themes = [k for k in modal_data if k.startswith(f"modal-codebook-{cat}-")]
        for pt in proj_themes:
            pt_pids = set(q["pid"] for q in modal_data[pt]["quotes"])
            for cb in codebook_themes:
                cb_pids = set(q["pid"] for q in modal_data[cb]["quotes"])
                if cb_pids and cb_pids.issubset(pt_pids):
                    mapping[pt] = cb
                    break
    return mapping


def rebuild_modal_data(modal_data, vetted):
    """Replace quotes in MODAL_DATA with vetted quotes."""
    proj_theme_map = build_proj_theme_mapping(modal_data)
    new_data = {}

    for key, group in modal_data.items():
        if key in vetted:
            # Direct match in vetted data
            new_data[key] = {
                "title": group["title"],
                "quotes": vetted[key]["quotes"],
            }
        elif key.startswith("modal-theme-"):
            # modal-theme-X-Y duplicates modal-codebook-X-Y
            cb_key = key.replace("modal-theme-", "modal-codebook-")
            if cb_key in vetted:
                new_data[key] = {
                    "title": group["title"],
                    "quotes": vetted[cb_key]["quotes"],
                }
            else:
                new_data[key] = group
        elif key.endswith("-theme") and key.startswith("modal-proj-"):
            # modal-proj-X-N-theme -> uses codebook theme quotes
            cb_key = proj_theme_map.get(key)
            if cb_key and cb_key in vetted:
                new_data[key] = {
                    "title": group["title"],
                    "quotes": vetted[cb_key]["quotes"],
                }
            else:
                new_data[key] = group
        elif key.endswith("-constraints") and key.startswith("modal-proj-"):
            # modal-proj-X-N-constraints -> uses constraints-{category}
            parts = key.split("-")
            # key format: modal-proj-{cat}-N-constraints
            cat = parts[2]
            # Handle multi-part category names (e.g., infrastructure_ops)
            # Find the number at the end before 'constraints'
            m = re.match(r"modal-proj-(.+)-(\d+)-constraints", key)
            if m:
                cat = m.group(1)
            constraint_key = f"constraints-{cat}"
            if constraint_key in vetted:
                new_data[key] = {
                    "title": group["title"],
                    "quotes": vetted[constraint_key]["quotes"],
                }
            else:
                new_data[key] = group
        else:
            new_data[key] = group

    return new_data


def update_button_counts(html, new_modal_data):
    """Update all 'View all N quotes' button text to match new quote counts."""
    def replace_btn(m):
        modal_id = m.group(1)
        suffix = m.group(2)  # e.g., "quotes &amp; rationale" or "supporting quotes"
        if modal_id in new_modal_data:
            new_count = len(new_modal_data[modal_id]["quotes"])
            return f"openModal('{modal_id}')\">View all {new_count} {suffix}<"
        return m.group(0)

    html = re.sub(
        r"openModal\('([^']+)'\)\">View all \d+ ([^<]+)<",
        replace_btn,
        html,
    )
    return html


def get_vetted_pids_for_theme(theme_key, vetted):
    """Get the set of vetted PIDs for a given theme panel key (panel-theme-X-Y -> modal-codebook-X-Y)."""
    cb_key = theme_key.replace("panel-theme-", "modal-codebook-")
    if cb_key in vetted:
        return set(q["pid"] for q in vetted[cb_key]["quotes"])
    return None


def get_vetted_pids_for_proj(panel_key, section_type, vetted, proj_theme_map):
    """Get vetted PIDs for a project panel's who/evidence/theme/constraints sections."""
    # panel_key format: panel-proj-{cat}-N
    m = re.match(r"panel-proj-(.+)-(\d+)", panel_key)
    if not m:
        return None
    cat, num = m.group(1), m.group(2)

    if section_type == "who":
        modal_key = f"modal-proj-{cat}-{num}-who"
        if modal_key in vetted:
            return set(q["pid"] for q in vetted[modal_key]["quotes"])
    elif section_type == "evidence":
        modal_key = f"modal-proj-{cat}-{num}-evidence"
        if modal_key in vetted:
            return set(q["pid"] for q in vetted[modal_key]["quotes"])
    elif section_type == "theme":
        modal_key = f"modal-proj-{cat}-{num}-theme"
        cb_key = proj_theme_map.get(modal_key)
        if cb_key and cb_key in vetted:
            return set(q["pid"] for q in vetted[cb_key]["quotes"])
    elif section_type == "constraints":
        constraint_key = f"constraints-{cat}"
        if constraint_key in vetted:
            return set(q["pid"] for q in vetted[constraint_key]["quotes"])
    return None


def filter_inline_quotes(html, vetted, modal_data):
    """Remove inline quote-blocks whose PID is not in the vetted set for that section."""
    # Build panel position index
    theme_panels = [(m.start(), m.group(1)) for m in re.finditer(r'id="(panel-theme-[^"]+)"', html)]
    proj_panels = [(m.start(), m.group(1)) for m in re.finditer(r'id="(panel-proj-[^"]+)"', html)]
    all_panels = sorted(theme_panels + proj_panels)

    # Build evidence-section and heading markers to determine who vs evidence in proj panels
    evidence_sections = [(m.start(), "evidence-section") for m in re.finditer(r'<div class="evidence-section">', html)]
    headings = [(m.start(), m.group(1)) for m in re.finditer(r"<h3[^>]*>([^<]+)</h3>", html)]

    proj_theme_map = build_proj_theme_mapping(modal_data)

    # Find the script boundary (JS code, not actual HTML quote-blocks)
    script_start = re.search(r"<script[^>]*>\s*var MODAL_DATA", html).start()

    # Process quote-blocks from end to start (so positions don't shift)
    qblock_pattern = re.compile(
        r'<div class="quote-block"><div class="quote-text">.*?</div>'
        r'(?:<span class="pid-badge">PID (\d+)</span>)?'
        r"(?:<div[^>]*>.*?</div>)*"  # optional rationale div
        r"</div>",
        re.DOTALL,
    )

    # Find all inline quote-blocks in actual HTML (not JS)
    blocks = list(qblock_pattern.finditer(html[:script_start]))
    removals = []

    for block in blocks:
        pos = block.start()
        pid_str = block.group(1)
        if not pid_str:
            # No PID badge - remove it
            removals.append((block.start(), block.end()))
            continue
        pid = int(pid_str)

        # Determine which panel this belongs to
        panel = None
        for pp, pn in all_panels:
            if pp > pos:
                break
            panel = pn

        if not panel:
            continue

        if panel.startswith("panel-theme-"):
            # Theme panel: check against vetted codebook quotes
            allowed_pids = get_vetted_pids_for_theme(panel, vetted)
            if allowed_pids is not None and pid not in allowed_pids:
                removals.append((block.start(), block.end()))

        elif panel.startswith("panel-proj-"):
            # Project panel: determine if this is who, evidence, theme, or constraints section
            # Find the nearest preceding heading
            section_type = None
            for hp, ht in sorted(headings, key=lambda x: x[0]):
                if hp > pos:
                    break
                heading_text = ht.lower()
                if "who it affects" in heading_text:
                    section_type = "who"
                elif "impact" in heading_text:
                    section_type = "evidence"
                elif "theme evidence" in heading_text:
                    section_type = "theme"
                elif "constraint" in heading_text:
                    section_type = "constraints"

            if section_type:
                allowed_pids = get_vetted_pids_for_proj(panel, section_type, vetted, proj_theme_map)
                if allowed_pids is not None and pid not in allowed_pids:
                    removals.append((block.start(), block.end()))

    # Apply removals from end to start
    result = html
    for start, end in sorted(removals, reverse=True):
        # Also remove trailing whitespace/newline
        while end < len(result) and result[end] in "\n\r \t":
            end += 1
        result = result[:start] + result[end:]

    print(f"  Removed {len(removals)} inline quote-blocks")
    return result


def find_constraint_blocks(html, limit):
    """Find all constraint-block divs by brace-matching, up to `limit` position."""
    blocks = []
    pos = 0
    while pos < limit:
        idx = html.find('<div class="constraint-block">', pos, limit)
        if idx == -1:
            break
        # Brace-match to find the end of the outermost div
        depth = 0
        i = idx
        while i < limit:
            if html[i : i + 4] == "<div":
                depth += 1
            if html[i : i + 6] == "</div>":
                depth -= 1
                if depth == 0:
                    end = i + 6
                    block_text = html[idx:end]
                    # Extract PID
                    pid_m = re.search(r"\(PID (\d+)\)", block_text)
                    pid = int(pid_m.group(1)) if pid_m else None
                    blocks.append((idx, end, pid, block_text))
                    break
            i += 1
        pos = idx + 1
    return blocks


def filter_inline_constraints(html, vetted):
    """Remove inline constraint-blocks whose PID is not in vetted constraints."""
    # Build panel position index
    all_panels = [(m.start(), m.group(1)) for m in re.finditer(r'id="(panel-(?:cat|proj)-[^"]+)"', html)]
    all_panels.sort()

    # Find script boundary
    script_start = re.search(r"<script[^>]*>\s*var MODAL_DATA", html).start()

    # Build vetted constraint PID sets per category
    vetted_constraint_pids = {}
    for cat in CATEGORIES:
        key = f"constraints-{cat}"
        if key in vetted:
            vetted_constraint_pids[cat] = set(q["pid"] for q in vetted[key]["quotes"])

    blocks = find_constraint_blocks(html, script_start)
    removals = []

    for start, end, pid, block_text in blocks:
        if pid is None:
            continue

        # Determine category from panel
        panel = None
        for pp, pn in all_panels:
            if pp > start:
                break
            panel = pn

        if not panel:
            continue

        # Extract category from panel name
        cat = None
        for c in CATEGORIES:
            if c in panel:
                cat = c
                break

        if cat and cat in vetted_constraint_pids:
            if pid not in vetted_constraint_pids[cat]:
                removals.append((start, end))

    # Apply removals from end to start
    result = html
    for start, end in sorted(removals, reverse=True):
        while end < len(result) and result[end] in "\n\r \t":
            end += 1
        result = result[:start] + result[end:]

    print(f"  Removed {len(removals)} inline constraint-blocks")
    return result


def main():
    print("Loading original HTML...")
    html = ORIGINAL.read_text(encoding="utf-8")
    orig_size = len(html)
    print(f"  Original size: {orig_size:,} chars ({orig_size / 1024 / 1024:.2f} MB)")

    print("Loading vetted quotes...")
    vetted = load_vetted_quotes()
    print(f"  Loaded {len(vetted)} vetted groups")

    print("Parsing MODAL_DATA...")
    modal_data, modal_var_start, modal_json_end = parse_modal_data(html)
    print(f"  Found {len(modal_data)} modal groups")

    print("Rebuilding MODAL_DATA with vetted quotes...")
    new_modal_data = rebuild_modal_data(modal_data, vetted)

    # Count changes
    changed = 0
    for key in modal_data:
        old_count = len(modal_data[key]["quotes"])
        new_count = len(new_modal_data[key]["quotes"])
        if old_count != new_count:
            changed += 1
    print(f"  Modified quote counts in {changed} groups")

    # Replace MODAL_DATA in HTML
    new_json = json.dumps(new_modal_data, ensure_ascii=False)
    # Reconstruct the var declaration
    # Find the exact 'var MODAL_DATA = ' prefix
    prefix_end = html.index("{", modal_var_start)
    new_var = html[modal_var_start:prefix_end] + new_json
    # Find the semicolon after the closing brace
    semi_pos = html.index(";", modal_json_end)
    html = html[:modal_var_start] + new_var + html[semi_pos:]

    print("Updating button counts...")
    html = update_button_counts(html, new_modal_data)

    print("Filtering inline quote-blocks...")
    html = filter_inline_quotes(html, vetted, modal_data)

    print("Filtering inline constraint-blocks...")
    html = filter_inline_constraints(html, vetted)

    # Write output
    print("Writing sanitized output...")
    OUTPUT.write_text(html, encoding="utf-8")
    new_size = len(html)
    reduction = (1 - new_size / orig_size) * 100
    print(f"  Output size: {new_size:,} chars ({new_size / 1024 / 1024:.2f} MB)")
    print(f"  Reduction: {reduction:.1f}%")

    # Validate basic HTML structure
    print("Validating output...")
    assert "<html" in html, "Missing <html> tag"
    assert "</html>" in html, "Missing </html> tag"
    assert "MODAL_DATA" in html, "Missing MODAL_DATA"
    assert html.count("<script") == html.count("</script>"), "Mismatched script tags"

    # Verify all vetted groups are present in new MODAL_DATA
    new_modal, _, _ = parse_modal_data(html)
    for key in vetted:
        if key.startswith("modal-"):
            assert key in new_modal, f"Missing vetted group: {key}"
            assert len(new_modal[key]["quotes"]) == len(vetted[key]["quotes"]), (
                f"Quote count mismatch for {key}: expected {len(vetted[key]['quotes'])}, got {len(new_modal[key]['quotes'])}"
            )
        elif key.startswith("constraints-"):
            # Constraints are distributed to proj constraint modals
            cat = key.replace("constraints-", "")
            proj_keys = [k for k in new_modal if k.startswith(f"modal-proj-{cat}-") and k.endswith("-constraints")]
            for pk in proj_keys:
                assert len(new_modal[pk]["quotes"]) == len(vetted[key]["quotes"]), (
                    f"Constraint count mismatch for {pk}: expected {len(vetted[key]['quotes'])}, got {len(new_modal[pk]['quotes'])}"
                )

    print("Done! Sanitized report written to:", OUTPUT)


if __name__ == "__main__":
    main()
