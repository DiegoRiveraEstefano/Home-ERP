/**
 * QuantityStepper Web Component
 * Domestic tactile quantity selector for pantry, chores, and expense items.
 * Example: <quantity-stepper name="quantity" value="1" min="1" max="99" step="1"></quantity-stepper>
 */
class QuantityStepper extends HTMLElement {
  connectedCallback() {
    if (this.querySelector('.stepper')) return;

    const name = this.getAttribute('name') || 'quantity';
    const min = parseFloat(this.getAttribute('min') ?? '0');
    const max = parseFloat(this.getAttribute('max') ?? '9999');
    const step = parseFloat(this.getAttribute('step') ?? '1');
    const initialValue = parseFloat(this.getAttribute('value') ?? min);

    this.innerHTML = `
      <div class="stepper" role="group" aria-label="Selector de cantidad">
        <button type="button" class="stepper-btn stepper-btn--dec" aria-label="Disminuir">-</button>
        <input type="number" class="stepper-input" name="${name}" value="${initialValue}" min="${min}" max="${max}" step="${step}">
        <button type="button" class="stepper-btn stepper-btn--inc" aria-label="Aumentar">+</button>
      </div>
    `;

    const input = this.querySelector('input');
    const btnDec = this.querySelector('.stepper-btn--dec');
    const btnInc = this.querySelector('.stepper-btn--inc');

    const updateState = () => {
      const val = parseFloat(input.value) || 0;
      btnDec.disabled = val <= min;
      btnInc.disabled = val >= max;
    };

    btnDec.addEventListener('click', () => {
      const current = parseFloat(input.value) || 0;
      if (current > min) {
        input.value = Math.max(min, current - step);
        input.dispatchEvent(new Event('change', { bubbles: true }));
        updateState();
      }
    });

    btnInc.addEventListener('click', () => {
      const current = parseFloat(input.value) || 0;
      if (current < max) {
        input.value = Math.min(max, current + step);
        input.dispatchEvent(new Event('change', { bubbles: true }));
        updateState();
      }
    });

    input.addEventListener('change', updateState);
    input.addEventListener('input', updateState);
    updateState();
  }
}

if (!customElements.get('quantity-stepper')) {
  customElements.define('quantity-stepper', QuantityStepper);
}
