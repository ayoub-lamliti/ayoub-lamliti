def update_section(content, marker_name, new_data):
    start_marker = f"<!-- {marker_name}-START -->"
    end_marker = f"<!-- {marker_name}-END -->"
    pattern = re.compile(rf"{start_marker}.*?{end_marker}", re.DOTALL)
    return pattern.sub(f"{start_marker}\n{new_data}\n{end_marker}", content)
