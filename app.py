from flask import Flask, request, render_template_string

app = Flask(__name__)

# Single-file template using Bootstrap for clean, immediate styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Carbon Footprint Awareness Platform</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; padding-top: 40px; }
        .card { box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .prompt-box { background-color: #212529; color: #32cd32; padding: 15px; border-radius: 5px; font-family: monospace; }
    </style>
</head>
<body>
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card mb-4">
                <div class="card-header bg-success text-white">
                    <h4 class="mb-0">Calculate Your Impact</h4>
                </div>
                <div class="card-body">
                    <form method="POST">
                        <div class="mb-3">
                            <label class="form-label">Transport Distance (km per week)</label>
                            <input type="number" class="form-control" name="transport" value="{{ request.form.get('transport', 100) }}" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Electricity Consumption (kWh per month)</label>
                            <input type="number" class="form-control" name="electricity" value="{{ request.form.get('electricity', 150) }}" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Diet Profile</label>
                            <select class="form-select" name="diet">
                                <option value="Balanced" {% if request.form.get('diet') == 'Balanced' %}selected{% endif %}>Balanced</option>
                                <option value="Meat-Heavy" {% if request.form.get('diet') == 'Meat-Heavy' %}selected{% endif %}>Meat-Heavy</option>
                                <option value="Vegetarian" {% if request.form.get('diet') == 'Vegetarian' %}selected{% endif %}>Vegetarian</option>
                                <option value="Vegan" {% if request.form.get('diet') == 'Vegan' %}selected{% endif %}>Vegan</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-success w-100">Calculate & Generate Insights</button>
                    </form>
                </div>
            </div>

            {% if results %}
            <div class="card">
                <div class="card-header bg-dark text-white">
                    <h4 class="mb-0">Emission Results & AI Prompt</h4>
                </div>
                <div class="card-body">
                    <h5>Monthly Emissions Breakdown:</h5>
                    <ul class="list-group mb-4">
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                            Transport
                            <span class="badge bg-primary rounded-pill">{{ results.transport }} kg CO2</span>
                        </li>
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                            Electricity
                            <span class="badge bg-warning text-dark rounded-pill">{{ results.electricity }} kg CO2</span>
                        </li>
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                            Diet
                            <span class="badge bg-info rounded-pill">{{ results.diet }} kg CO2</span>
                        </li>
                        <li class="list-group-item d-flex justify-content-between align-items-center active bg-danger border-danger">
                            <strong>Total Footprint</strong>
                            <span><strong>{{ results.total }} kg CO2</strong></span>
                        </li>
                    </ul>

                    <h5>Generated AI Prompt:</h5>
                    <p class="text-muted small">This is the engineered prompt ready to be sent to an LLM to generate user-specific reduction strategies.</p>
                    <div class="prompt-box">
                        {{ prompt }}
                    </div>
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    ai_prompt = None

    if request.method == 'POST':
        # 1. Gather inputs
        transport_km_week = float(request.form['transport'])
        electricity_kwh_month = float(request.form['electricity'])
        diet = request.form['diet']

        # 2. Calculate footprint (Monthly estimates)
        transport_co2 = round((transport_km_week * 4) * 0.2, 2)
        electricity_co2 = round(electricity_kwh_month * 0.8, 2)
        
        diet_base = {"Balanced": 150, "Meat-Heavy": 250, "Vegetarian": 90, "Vegan": 60}
        diet_co2 = diet_base.get(diet, 150)

        total_co2 = round(transport_co2 + electricity_co2 + diet_co2, 2)

        results = {
            "transport": transport_co2,
            "electricity": electricity_co2,
            "diet": diet_co2,
            "total": total_co2
        }

        # 3. Determine highest category for targeted prompt engineering
        categories = {"Transport": transport_co2, "Electricity": electricity_co2, "Diet": diet_co2}
        highest_category = max(categories, key=categories.get)

        # 4. Construct the PromptWars engineered string
        ai_prompt = f"""System Role: You are an expert environmental consultant.
User Data: Total monthly footprint is {total_co2} kg CO2. 
Breakdown: Transport ({transport_co2} kg), Electricity ({electricity_co2} kg), Diet ({diet_co2} kg - {diet} profile).
Task: The user's highest emission category is {highest_category}. Generate 3 highly specific, actionable, and low-cost strategies to reduce their emissions in this specific category. Format as a bulleted list."""

    return render_template_string(HTML_TEMPLATE, results=results, prompt=ai_prompt)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)