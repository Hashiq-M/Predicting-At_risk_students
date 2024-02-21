from flask import Flask, render_template, request
import io  # For in-memory image handling
import matplotlib.pyplot as plt  # For graph generation
import base64
import matplotlib
import student_data
import time

matplotlib.use('Agg')
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # Display your HTML form here

@app.route("/process", methods=["POST"])
def process_form():
    gpa = int(request.form["GPA"])
    mark = int(request.form["Mark"])
    atd = int(request.form["Atd"])
    hrs = int(request.form["St_hr"])

    left = [1, 2, 3, 4]
    height = [gpa, mark, atd, hrs]
    tick_label = ["GPA", "Exam_Score", "Attendance", "Study"]

    plt.figure(figsize=(8, 6))  # Adjust figure size as needed
    plt.ylim(0, 100)
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red', 'green', 'blue', 'violet'])
    plt.xlabel("Student Performance")
    plt.ylabel("Evaluation")
    plt.title("At-Risk Student Prediction")

    # Create an in-memory image buffer
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png")
    plt.savefig("graph.png")
    plt.close()  # Ensure figure is closed to avoid memory leaks

    # Convert image buffer to base64 for use in HTML
    # Correctly handle binary image data:
    img_data = img_buffer.getvalue()  # No decoding needed
    img_b64 = f"data:image/png;base64,{base64.b64encode(img_data).decode('utf-8')}"

    # Call the predictRisk function
    prediction_results , prediction_probabilities = student_data.predictRisk("graph.png")
    return render_template("result.html", img_b64=img_b64, prediction_results=prediction_results,  prediction_probabilities=prediction_probabilities)

if __name__ == "__main__":
    app.run(debug=True)  # Set debug=False for production
