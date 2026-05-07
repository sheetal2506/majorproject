
from flask import Flask, request, jsonify, render_template
from cnn_model import predict_body_shape

app = Flask(__name__)

# ------------------ PAGE ROUTES ------------------

@app.route('/')
def home():
    return render_template('frontpage.html')

@app.route('/firstpage')
def firstpage():
    return render_template('firstpage.html')

@app.route('/secondpage')
def secondpage():
    return render_template('secondpage.html')

@app.route('/fifthpage')
def fifthpage():
    return render_template('fifthpage.html')



@app.route('/occasion')
def occasion():
    return render_template('occasion.html')

@app.route('/signup')
def signup():
    return render_template('signuppage.html')

@app.route('/imagestore')
def imagestore():
    return render_template('imagestore.html')

# 👉 Add this ONLY if you have tryon.html
@app.route('/tryon')
def tryon():
    return render_template('tryon.html')


# ------------------ AI LOGIC ------------------

def get_outfit(body_type, occasion):

    outfits = {

        "pear": {
            "casual": {
                "suggestion": ["Statement Tops", "A-Line & Wide leg Bottoms", "High-Waist Bottoms"],
                "avoid": ["Avoid tight bottoms","Heavy Prints","Low-Rise Jeans","Tight Skirts"],
                "images": ["static/pearcasual1.jpg", "static/pearcasual2.jpg", "static/pearcasual3.jpg"]
            },
            "party": {
                "suggestion": ["Off-shoulder dress", "Flare dress"],
                "avoid": "Avoid bodycon dresses",
                "images": ["static/pearparty1.jpg", "static/pearparty2.jpg"]
            },
            "interview": {
                "suggestion": ["Structured blazer", "Straight pants"],
                "avoid": "Avoid tight leggings",
                "images": ["static/pearformals.jpg"]
            }
        },

        "hourglass": {
            "casual": {
                "suggestion": ["Fitted tops", "High waist jeans"],
                "avoid": "Avoid loose shapeless outfits",
                "images": ["static/hourcasual1.jpg", "static/hourcasual2.jpg"]
            },
            "party": {
                "suggestion": ["Bodycon dress", "Wrap dress"],
                "avoid": "Avoid oversized outfits",
                "images": ["static/hourparty1.jpg", "static/hourparty2.jpg"]
            },
            "interview": {
                "suggestion": ["Pencil skirt", "Formal shirt","Blazor","Tailored trousers"],
                "avoid": "Avoid baggy clothes",
                "images": ["static/hourformals1.jpg", "static/hourformals2.jpg"]
            }
        },

        "rectangle": {
            "casual": {
                "suggestion": ["Layered outfits", "Peplum tops"],
                "avoid": "Avoid straight shapeless dresses",
                "images": ["static/rectanglecasual1.jpg", "static/rectanglecasual2.jpg"]
            },
            "party": {
                "suggestion": ["Ruffled dress", "Skater dress"],
                "avoid": "Avoid plain straight cuts",
                "images": ["static/rectangleparty1.jpg", "static/rectangleparty2.jpg"]
            },
            "interview": {
                "suggestion": ["Blazer + belt", "Structured outfits"],
                "avoid": "Avoid loose clothes",
                "images": ["static/rectangleformals1.jpg"]
            }
        },

        "inverted_triangle": {
            "casual": {
                "suggestion": ["V-neck tops", "Wide leg pants"],
                "avoid": "Avoid shoulder pads",
                "images": ["static/invertedtrianglecasual1.jpg", "static/invertedtrianglecasual2.jpg","static/invertedtrianglecasual3.jpg"]
            },
            "party": {
                "suggestion": ["A-line skirts", "Flowy dresses"],
                "avoid": "Avoid heavy tops",
                "images": ["static/invertedparty1.jpg", "static/invertedparty2.jpg","static/invertedparty3.jpg"]
            },
            "interview": {
                "suggestion": ["Simple tops + dark bottoms"],
                "avoid": "Avoid puff sleeves",
                "images": ["static/invertedformals1.jpg"]
            }
        }
    }

    # fallback safety
    return outfits.get(body_type, {}).get(occasion, {
        "suggestion": ["Try balanced outfits"],
        "avoid": "Avoid extreme styles",
        "images": []
    })


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json

        import base64

        # Check image
        if not data.get('image'):
            return jsonify({"error": "No image received"})

        # Decode image
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)

        with open("static/temp.jpg", "wb") as f:
            f.write(image_bytes)

        # Run AI
        image_path = "static/temp.jpg"
        from cnn_model import predict_body_shape

        body_type = predict_body_shape(image_path)
        print("Detected body type:", body_type)  # DEBUG

        # Fallback
        if body_type is None:
            print("Using fallback ML model")
            body_type = predict_body_type(34, 28, 36)

        occasion = data.get('occasion', 'casual').lower()
        body_type = body_type.lower()

        result = get_outfit(body_type, occasion)
        print("Body Type:", body_type)
        print("Occasion:", occasion)

        return jsonify({
    "body_type": body_type,
    "suggestion": result["suggestion"],
    "avoid": result["avoid"],
    "images": result.get("images", []) 
})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)})
   


# ------------------ RUN APP ------------------

if __name__ == '__main__':
    app.run(debug=True)