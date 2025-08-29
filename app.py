
from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)


FULL_NAME_LOWER = "swati_sucharita_samantaray"
DOB_DDMMYYYY   = "11072004"
EMAIL_ID       = "swati@gmail.com"
ROLL_NUMBER    = "22BAI10040"


USER_ID = f"{FULL_NAME_LOWER}_{DOB_DDMMYYYY}"

def split_categories(items):
    even_numbers = []
    odd_numbers = []
    alphabets = []
    special_chars = []
    letter_stream = [] 

    for raw in items:
        s = "" if raw is None else str(raw)

        # Gather letters for the letter stream from ANY token
        for ch in s:
            if ch.isalpha():
                letter_stream.append(ch)

        if s.isdigit():
            n = int(s)
            (even_numbers if n % 2 == 0 else odd_numbers).append(s)
        elif s.isalpha():
            alphabets.append(s.upper())
        else:
            special_chars.append(s)

    return even_numbers, odd_numbers, alphabets, special_chars, letter_stream

def alternating_caps_reverse(letters):
    rev = list(reversed(letters))
    out_chars = []
    upper_next = True
    for ch in rev:
        out_chars.append(ch.upper() if upper_next else ch.lower())
        upper_next = not upper_next
    return "".join(out_chars)

@app.route("/bfhl", methods=["POST"])
def bfhl():
    try:
        body = request.get_json(force=True, silent=False) or {}
        data = body.get("data", [])
        if not isinstance(data, list):
            raise ValueError("'data' must be a JSON array")

        even_numbers, odd_numbers, alphabets, special_chars, letters = split_categories(data)
        total = 0
        for s in even_numbers + odd_numbers:
            try:
                total += int(s)
            except ValueError:
                pass

        concat_str = alternating_caps_reverse(letters)

        resp = {
            "is_success": True,
            "user_id": USER_ID,
            "email": EMAIL_ID,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": special_chars,
            "sum": str(total),
            "concat_string": concat_str
        }
        return jsonify(resp), 200
    except Exception as e:
        return jsonify({
            "is_success": False,
            "error": str(e)
        }), 200

#health check
@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "ok", "route": "/bfhl", "method": "POST"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)