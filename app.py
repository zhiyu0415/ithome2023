import openai
import os
from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)

# 設置 OpenAI API 金鑰
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        text_input = request.form['restaurant']
        select_menu = request.form['restaurant-region']
        restaurant = request.form["restaurant"]
        combined_prompt = f"Recommend me some restaurants in {select_menu} such as {restaurant}"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(combined_prompt),
            max_tokens=256,
            temperature=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return redirect(url_for("index", result=response.choices[0].text))


    result = request.args.get("result")
    return render_template("index.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)

def generate_prompt(restaurant):
    return """Recommend me some restaurants in northern Taiwan such as hotpot restaurants

    I want to generate "restaurant name - region"

    region:
    Northern Taiwan:
    Taipei City, New Taipei City, Keelung City, Taoyuan City, Yilan County, Hsinchu County, Hsinchu City

    Central Taiwan: 
    Miaoli County, Taichung City, Changhua County, Nantou County, Yunlin County

    Southern Taiwan: Chiayi County, Chiayi City, Tainan City, Kaohsiung City, Pingtung County

    Eastern Taiwan: Yilan County, Hualien County, Taitung County

    Taiwan's outlying islands: Penghu, Kinmen, Matsu, Green Island, Orchid Island, Xiaoliuqiu
restaurant-type:hotpot
restaurant:1. Steamy Pot - Taipei City
2. Spicy Delight - Keelung City
3. Sizzling Bowl - New Taipei City
4. Hot n' Savory - Taoyuan City
5. Firewood Hotpot - Hsinchu City
restaurant-type: {}
restaurant:""".format(
        restaurant.capitalize()
    )
