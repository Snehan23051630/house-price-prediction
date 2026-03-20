from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from .model import predict_price

# ── Blueprints ────────────────────────────────────────────────────────────────
main  = Blueprint('main',  __name__)
auth  = Blueprint('auth',  __name__)
api   = Blueprint('api',   __name__, url_prefix='/api')

# ── Main pages ────────────────────────────────────────────────────────────────

@main.route('/')
def index():
    """Home page — house price predictor form."""
    return render_template('index.html')


@main.route('/about')
def about():
    """About page explaining the model and project."""
    return render_template('about.html')


# ── Auth pages ────────────────────────────────────────────────────────────────

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login page (demo — no real auth)."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Demo credentials — replace with real DB lookup in production
        if username == 'demo' and password == 'demo123':
            session['user'] = username
            flash('Welcome back, demo!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


# ── API endpoints ─────────────────────────────────────────────────────────────

@api.route('/predict', methods=['POST'])
def predict():
    """
    POST /api/predict
    Body: { "sqft": 1800, "bedrooms": 3 }
    Returns: { "price": 360000.0, "formatted": "$360,000" }
    """
    from flask import current_app

    try:
        body = request.get_json(force=True)
        if not body:
            return jsonify({'error': 'Request body must be JSON.'}), 400

        sqft     = float(body.get('sqft', 0))
        bedrooms = float(body.get('bedrooms', 1))

        model  = current_app.config['MODEL']
        result = predict_price(model, sqft, bedrooms)
        return jsonify(result)

    except (ValueError, TypeError) as exc:
        return jsonify({'error': str(exc)}), 400
    except Exception:
        return jsonify({'error': 'Prediction failed. Please try again.'}), 500


@api.route('/health', methods=['GET'])
def health():
    """Simple health-check endpoint used by Render/Railway."""
    return jsonify({'status': 'ok', 'model': 'loaded'})
