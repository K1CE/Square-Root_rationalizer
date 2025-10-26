#########IMPORTS
import sys
import time
import math



#########CLASSES

# Simple object for storing data in groups.
# Represents a multiplier that approximates a number when it was multiplied by a square root.
class Data_Point():

    def __init__(self, approximates, distance, multiplier, text="goal"):
        """
        Initializes a Data_Point object.
        
        Args:
            approximates (list[float]): The list of approximate whole numbers/goal multiples.
            distance (float): The average distance from the ideal integer/goal multiple.
            multiplier (float): The multiplier that produced these approximations.
            text (str): A label for this data point (e.g., "integer", "goal", "mention").
        """
        self.approximates = approximates
        self.distance = distance
        self.multiplier = multiplier
        self.text = text
    
    # Allows Data_Point objects to be compared based on their absolute distance.
    # Essential for sorting honorable mentions (closer distance is "less than").
    def __lt__(self, other):
        return abs(self.distance) < abs(other.distance)
        
    def __eq__(self, other):
        return math.isclose(abs(self.distance), abs(other.distance))
        
    def __repr__(self):
        """A simple representation for debugging."""
        return f"Data_Point(m={self.multiplier}, d={self.distance:.6f}, t='{self.text}')"


#########FUNCTIONS

def is_number_tryexcept(s):
    """ Returns True if string can be converted to a float. """
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False

def attempt_convert_scientific_notation(s):
    """
    Converts a string to a float, handling scientific notation (e.g., '1e-5').
    If the string is not convertible, it returns the original string.
    """
    s_str = str(s).lower() # Ensure s is a string and lowercase for 'e'
    index = s_str.find('e')
    if index >= 0:
        s1 = s_str[0:index]
        s2 = s_str[index + 1:]
        if is_number_tryexcept(s1) and is_number_tryexcept(s2):
            return float(s1) * (10 ** float(s2))
    
    if is_number_tryexcept(s):
        return float(s)
    
    return s # Return original string if not convertible


def find_match(values, multiplier, goal, text, distance_limit):
    """
    Calculates the average distance of a set of values to the closest multiples of a goal.
    
    Args:
        values (list[float]): The calculated results for the current multiplier.
        multiplier (float): The current multiplier.
        goal (float): The target multiple (e.g., 1 for integers, user's custom goal).
        text (str): Descriptive text for the Data_Point (e.g., "integer", "goal").
        distance_limit (float): The maximum absolute average distance allowed for a match.
    
    Returns:
        Data_Point or None: A Data_Point object if a match is found, otherwise None.
    """
    if not values:
        return None

    average_distance = 0.0
    approximates = []
    
    for val in values:
        distance_to_goal_multiple = ((val + (goal / 2)) % goal) - (goal / 2)
        average_distance += abs(distance_to_goal_multiple)
        approximates.append(val - distance_to_goal_multiple)
    
    average_distance = average_distance / len(values)
    
    if abs(average_distance) < distance_limit:
        return Data_Point(approximates, average_distance, multiplier, text)
    
    return None


def store_mention(data, mentions_list, max_mentions):
    """
    Stores a Data_Point in the mentions_list, maintaining it sorted by distance.
    
    Args:
        data (Data_Point): The new Data_Point to potentially store.
        mentions_list (list[Data_Point]): The current list of honorable mentions.
        max_mentions (int): The maximum number of mentions to store.
    """
    if len(mentions_list) < max_mentions:
        mentions_list.append(data)
        mentions_list.sort()
    elif data < mentions_list[-1]:
        mentions_list[-1] = data
        mentions_list.sort()


def _format_result_string(data_point, original_radicands_list):
    """
    Formats a Data_Point into a human-readable string.
    """
    if not data_point or data_point.distance > 1000:
        return "No suitable match found."

    num_radicands = len(original_radicands_list)
    multiplier = data_point.multiplier
    targets = data_point.approximates
    distance = data_point.distance

    result_lines = []
    
    if num_radicands <= 1:
        result_lines.append(f"    >> {multiplier:.6g} * √{original_radicands_list[0]} <<")
        result_lines.append(f"    approximating: {targets[0]:.6f}")
        result_lines.append(f"    with a distance of {abs(distance):.6g}")
    else:
        radicand_str_parts = [f"√{r:.6g}" for r in original_radicands_list]
        result_lines.append(f"    >> {multiplier:.6g} * ({' OR '.join(radicand_str_parts)}) <<")
        
        approx_targets_str = ", ".join([f"{t:.6f}" for t in targets])
        result_lines.append(f"    approximating: {approx_targets_str}")
        result_lines.append(f"    with an average distance of {abs(distance):.6g}")
    
    return "\n".join(result_lines)

def _generate_svg_graphic(points, x_limit, y_limit):
    """
    Generates an SVG scatter plot of multipliers vs. distances.
    
    Args:
        points (list[Data_Point]): A list of all data points found.
        x_limit (float): The maximum multiplier value (for X-axis).
        y_limit (float): The maximum distance value (for Y-axis).

    Returns:
        str: A string containing the SVG data.
    """
    if not points:
        return "<svg width='500' height='300'><text x='50' y='150'>No data points to plot.</text></svg>"
    
    WIDTH, HEIGHT = 500, 300
    PAD = 40

    # Filter out placeholder points with huge distances
    plot_points = [p for p in points if p.distance < 1000]
    if not plot_points:
        return "<svg width='500' height='300'><text x='50' y='150'>No valid data points to plot.</text></svg>"
        
    max_dist = max(abs(p.distance) for p in plot_points) if plot_points else y_limit

    def scale(x, y):
        px = PAD + (x / x_limit) * (WIDTH - 2 * PAD)
        py = HEIGHT - PAD - (abs(y) / max_dist) * (HEIGHT - 2 * PAD)
        return px, py

    svg = [f'<svg width="{WIDTH}" height="{HEIGHT}" xmlns="http://www.w3.org/2000/svg">']
    svg.append('<style>.small { font: italic 10px sans-serif; } .label { font: bold 12px sans-serif; }</style>')
    # Axes
    svg.append(f'<line x1="{PAD}" y1="{HEIGHT - PAD}" x2="{WIDTH - PAD}" y2="{HEIGHT - PAD}" stroke="black"/>')
    svg.append(f'<line x1="{PAD}" y1="{PAD}" x2="{PAD}" y2="{HEIGHT - PAD}" stroke="black"/>')
    svg.append(f'<text x="{WIDTH/2}" y="{HEIGHT - 5}" class="label">Multiplier</text>')
    svg.append(f'<text x="5" y="{HEIGHT/2}" transform="rotate(-90 15,{HEIGHT/2})" class="label">Distance</text>')
    svg.append(f'<text x="{PAD}" y="{HEIGHT - PAD + 15}" class="small">0</text>')
    svg.append(f'<text x="{WIDTH - PAD}" y="{HEIGHT - PAD + 15}" class="small">{x_limit:.2g}</text>')
    svg.append(f'<text x="{PAD-5}" y="{PAD}" text-anchor="end" class="small">{max_dist:.2g}</text>')

    # Points
    for p in plot_points:
        px, py = scale(p.multiplier, p.distance)
        color = "blue" if "integer" in p.text else "green" if "goal" in p.text else "gray"
        svg.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="3" fill="{color}"/>')

    svg.append('</svg>')
    return '\n'.join(svg)

def rationalize_sqrt_results(radicands_input, limit=20, increment=1, goal=None, root_index=2):
    """
    Calculates multipliers for roots that approximate whole numbers or goal multiples,
    and returns the results in a paginated, structured format.

    This function finds multipliers (N) such that N * root(R, root_index) is close to
    an integer or a multiple of a specified goal, where R is the radicand.

    Args:
        radicands_input (list[float] or list[str]): A list of radicand values.
        limit (float or str, optional): The upper limit for the multiplier. Defaults to 20.
        increment (float or str, optional): The step size for the multiplier. Defaults to 1.
        goal (float, str or None, optional): A custom multiple to target. If None or invalid, 
                                            it defaults to the increment value. Defaults to None.
        root_index (int, optional): The index of the root (e.g., 2 for square root). Defaults to 2.

    Returns:
        list[dict]: A list where each dictionary represents a page of results.
            Each dictionary has the format:
            {
                'page_id': str,      # e.g., 'main_result', 'honorable_mentions', 'graphic'
                'title': str,      # A human-readable title for the page.
                'content': str,    # The formatted content for the page.
            }
    """
    # --- 1. Input Validation and Sanitization ---
    radicands = [float(r) for r in radicands_input if is_number_tryexcept(r)]
    if not radicands:
        raise ValueError("radicands_input must contain at least one valid number.")

    limit_val = attempt_convert_scientific_notation(limit) or 20
    increment_val = attempt_convert_scientific_notation(increment) or 1
    goal_val = attempt_convert_scientific_notation(goal)
    if not isinstance(goal_val, (int, float)):
        goal_val = increment_val
    using_goal = not math.isclose(goal_val, 1.0)

    # --- 2. Initialization ---
    MAX_MENTIONS = 10
    iterations = int(limit_val / increment_val)
    
    # Use a dynamic distance limit for goal-seeking, starting at 10% of the goal value
    goal_distance_limit = goal_val / 10
    
    best_integer_data = Data_Point([0], 10001, 0, "integer")
    best_goal_data = Data_Point([0], 10002, 0, "goal")
    mentions = []
    all_points_for_graphic = []

    # --- 3. Main Calculation Loop ---
    for i in range(1, iterations + 1):
        multiplier = increment_val * i
        results = [multiplier * (r ** (1 / root_index)) for r in radicands]
        
        # Check for proximity to integers (goal=1)
        data_int = find_match(results, multiplier, 1.0, "integer", 0.1)
        if data_int and data_int < best_integer_data:
            best_integer_data = data_int
            all_points_for_graphic.append(data_int)

        # Check for proximity to the custom goal, if specified
        if using_goal:
            data_goal = find_match(results, multiplier, goal_val, "goal", goal_distance_limit)
            if data_goal:
                all_points_for_graphic.append(data_goal)
                if data_goal < best_goal_data:
                    best_goal_data = data_goal
                    # Tighten the distance limit when a new best is found
                    new_dist = abs(best_goal_data.distance)
                    goal_distance_limit -= (goal_distance_limit - new_dist) / MAX_MENTIONS
                else:
                    store_mention(data_goal, mentions, MAX_MENTIONS)

    # --- 4. Assemble Output Pages ---
    pages = []

    # Page 1: Main Results
    main_content_parts = ["--- Best Match for Integer ---", _format_result_string(best_integer_data, radicands)]
    if using_goal:
        main_content_parts.append("\n--- Best Match for Goal ---")
        main_content_parts.append(_format_result_string(best_goal_data, radicands))
    pages.append({
        'page_id': 'main_result',
        'title': 'Main Results',
        'content': "\n".join(main_content_parts)
    })

    # Page 2: Honorable Mentions
    if mentions:
        mention_content = "\n\n".join([_format_result_string(m, radicands) for m in mentions])
        pages.append({
            'page_id': 'honorable_mentions',
            'title': 'Honorable Mentions',
            'content': mention_content
        })

    # Page 3: Graphic
    graphic_svg = _generate_svg_graphic(all_points_for_graphic, limit_val, goal_val / 10)
    pages.append({
        'page_id': 'graphic',
        'title': 'Distance vs. Multiplier Plot',
        'content': graphic_svg
    })

    return pages