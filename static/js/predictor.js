/**
 * predictor.js
 * Handles the bedroom slider sync and the /api/predict Fetch call.
 */

(function () {
  'use strict';

  // ── DOM refs ───────────────────────────────────────────────────────────────
  const sqftInput    = document.getElementById('sqft');
  const bedroomSlider = document.getElementById('bedrooms');
  const bedCount     = document.getElementById('bed-count');
  const bedLabel     = document.getElementById('bed-label');
  const predictBtn   = document.getElementById('predict-btn');
  const resultBox    = document.getElementById('result');
  const errorBox     = document.getElementById('error-msg');
  const priceEl      = document.getElementById('result-price');
  const subtextEl    = document.getElementById('result-subtext');

  // ── Bedroom slider ─────────────────────────────────────────────────────────
  bedroomSlider.addEventListener('input', () => {
    bedCount.textContent = bedroomSlider.value;
    bedLabel.textContent = bedroomSlider.value;
  });

  // ── Enter key shortcut ─────────────────────────────────────────────────────
  sqftInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') predictPrice();
  });

  // ── Button click ───────────────────────────────────────────────────────────
  predictBtn.addEventListener('click', predictPrice);

  // ── Core prediction function ───────────────────────────────────────────────
  async function predictPrice() {
    const sqft     = parseFloat(sqftInput.value);
    const bedrooms = parseInt(bedroomSlider.value, 10);

    // Reset UI
    resultBox.classList.remove('show');
    errorBox.classList.remove('show');

    // Client-side validation
    if (!sqftInput.value || isNaN(sqft) || sqft < 100) {
      showError('Please enter a valid square footage (minimum 100 sq ft).');
      sqftInput.focus();
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('/api/predict', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ sqft, bedrooms }),
      });

      const data = await response.json();

      if (!response.ok || data.error) {
        showError(data.error || 'Prediction failed. Please try again.');
        return;
      }

      const formatted = new Intl.NumberFormat('en-IN', {
        style:                 'currency',
        currency:              'INR',
        maximumFractionDigits: 0,
      }).format(data.price);

      priceEl.textContent   = formatted;
      subtextEl.textContent = `For a ${sqft.toLocaleString()} sq ft home with ${bedrooms} bedroom${bedrooms > 1 ? 's' : ''}`;
      resultBox.classList.add('show');

    } catch (_err) {
      showError('Network error — please check your connection and try again.');
    } finally {
      setLoading(false);
    }
  }

  // ── Helpers ────────────────────────────────────────────────────────────────
  function showError(msg) {
    errorBox.textContent = msg;
    errorBox.classList.add('show');
  }

  function setLoading(on) {
    predictBtn.disabled = on;
    predictBtn.classList.toggle('loading', on);
  }

})();
