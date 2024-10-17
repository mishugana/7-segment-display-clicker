import tkinter as tk

def main():
    # Create the main window
    root = tk.Tk()
    root.title("7-Segment Display Selector")

    # Create a canvas to draw the segments
    canvas = tk.Canvas(root, width=200, height=300)
    canvas.pack()

    # Define the coordinates for each segment
    segments = {
        'A': [(50, 20), (150, 20), (140, 30), (60, 30)],
        'B': [(150, 20), (160, 30), (160, 120), (150, 130), (140, 120), (140, 30)],
        'C': [(150, 140), (160, 150), (160, 240), (150, 250), (140, 240), (140, 150)],
        'D': [(50, 250), (150, 250), (140, 240), (60, 240)],
        'E': [(40, 140), (50, 150), (50, 240), (40, 250), (30, 240), (30, 150)],
        'F': [(40, 20), (50, 30), (50, 120), (40, 130), (30, 120), (30, 30)],
        'G': [(50, 130), (150, 130), (140, 140), (60, 140)],
    }

    # Store the canvas IDs and states of each segment
    segment_ids = {}
    segment_states = {key: False for key in segments.keys()}

    # List to store recorded values
    recorded_values = []

    # Function to toggle segment state
    def toggle_segment(event):
        for key, seg_id in segment_ids.items():
            if canvas.find_withtag('current')[0] == seg_id:
                # Toggle the segment state
                segment_states[key] = not segment_states[key]
                # Update the segment color
                color = 'red' if segment_states[key] else 'white'
                canvas.itemconfig(seg_id, fill=color)
                # Update the displayed value
                update_output()
                break

    # Draw the segments on the canvas
    for key, coords in segments.items():
        seg_id = canvas.create_polygon(coords, fill='white', outline='black', width=2)
        segment_ids[key] = seg_id
        canvas.tag_bind(seg_id, '<Button-1>', toggle_segment)

    # Function to get the decimal value of the current segment selection
    def get_decimal_value():
        # Order of segments for the code
        order = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        # Create the segment code string
        code = ''.join(['1' if segment_states[seg] else '0' for seg in order])
        # Convert the binary code to decimal
        decimal_value = int(code, 2)
        return decimal_value

    # Label to display the current decimal value
    output_label = tk.Label(root, text="Current Value: 0", font=("Helvetica", 16))
    output_label.pack(pady=10)

    # Function to update the output label
    def update_output():
        decimal_value = get_decimal_value()
        output_label.config(text=f"Current Value: {decimal_value}")

    # Function to record the current value and update the list
    def record_value():
        decimal_value = get_decimal_value()
        recorded_values.append(decimal_value)
        # Update the label showing the list of values
        values_label.config(text=f"Recorded Values: {recorded_values}")

    # Button to record the value
    record_button = tk.Button(root, text="Record Value", command=record_value)
    record_button.pack(pady=10)

    # Function to clear recorded values
    def clear_values():
        recorded_values.clear()
        values_label.config(text="Recorded Values: []")

    # Button to clear the recorded values
    clear_button = tk.Button(root, text="Clear Values", command=clear_values)
    clear_button.pack(pady=5)

    # Label to display the recorded values
    values_label = tk.Label(root, text="Recorded Values: []", font=("Helvetica", 12))
    values_label.pack(pady=10)

    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
