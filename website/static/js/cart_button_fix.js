/**
 * CART BUTTON FIX
 * ─────────────────────────────────────────────────────────────
 * Problem: Clicking the "Add to Cart" / "+" button causes it to
 *          change and show the cart amount instead of keeping its
 *          original appearance.
 *
 * Root cause: The AJAX success handler was likely updating the
 *             button's innerHTML/text with the cart amount, and/or
 *             the button was not being restored after the request.
 *
 * HOW TO USE:
 *   Include this script at the bottom of your base.html or any
 *   template that has "Add to Cart" buttons, AFTER jQuery.
 *
 *   <script src="{{ url_for('static', filename='js/cart_button_fix.js') }}"></script>
 *
 * ─────────────────────────────────────────────────────────────
 */

(function () {
  /**
   * Intercepts all "Add to Cart" clicks.
   * Stores the original button HTML before the AJAX call and
   * restores it afterwards — so the button never shows amounts.
   */
  document.addEventListener('DOMContentLoaded', function () {

    // ── 1. Intercept clicks on ANY add-to-cart link or button ──────────────
    document.body.addEventListener('click', function (e) {
      const btn = e.target.closest(
        'a[href*="add-to-cart"], button[data-cart], .add-to-cart-btn, [class*="add-cart"]'
      );
      if (!btn) return;

      // Save original content immediately
      const originalHTML = btn.innerHTML;
      const originalDisabled = btn.disabled;

      // Show brief loading state WITHOUT changing the button shape/text permanently
      btn.disabled = true;
      btn.style.opacity = '0.7';

      // After 1.5 s, always restore the button regardless of AJAX outcome
      // (The real restoration also happens in the fetch/$.ajax success below)
      const safetyRestore = setTimeout(() => {
        restoreButton(btn, originalHTML, originalDisabled);
      }, 1500);

      // Store on element so the AJAX callback can find it
      btn._originalHTML = originalHTML;
      btn._originalDisabled = originalDisabled;
      btn._safetyRestore = safetyRestore;
    });

    // ── 2. Patch jQuery AJAX if jQuery is present ─────────────────────────
    if (window.jQuery) {
      const originalAjax = jQuery.ajax;
      jQuery.ajax = function (settings) {
        const url = (settings.url || '').toString();
        if (url.includes('add-to-cart') || url.includes('pluscart') || url.includes('minuscart')) {
          const originalSuccess = settings.success;
          settings.success = function (data) {
            // Call the original success handler
            if (originalSuccess) originalSuccess.apply(this, arguments);

            // After the handler runs, find any button that was mutated and fix it
            requestAnimationFrame(function () {
              document.querySelectorAll(
                'a[href*="add-to-cart"], button[data-cart], .add-to-cart-btn'
              ).forEach(btn => {
                if (btn._originalHTML) {
                  restoreButton(btn, btn._originalHTML, btn._originalDisabled);
                }
              });

              // Update ONLY the cart count badge — never the button text
              updateCartBadge(data);
            });
          };
        }
        return originalAjax.call(this, settings);
      };
    }

    // ── 3. Patch native fetch ─────────────────────────────────────────────
    const originalFetch = window.fetch;
    window.fetch = function (input, init) {
      const url = (typeof input === 'string' ? input : input.url || '').toString();
      const promise = originalFetch.apply(this, arguments);

      if (url.includes('add-to-cart') || url.includes('pluscart') || url.includes('minuscart')) {
        promise.then(res => res.clone().json().then(data => {
          requestAnimationFrame(function () {
            // Restore any button that stored its original HTML
            document.querySelectorAll('[data-original-html]').forEach(btn => {
              restoreButton(btn, btn.dataset.originalHtml, false);
            });
            document.querySelectorAll('a[href*="add-to-cart"], button[data-cart], .add-to-cart-btn').forEach(btn => {
              if (btn._originalHTML) {
                restoreButton(btn, btn._originalHTML, btn._originalDisabled);
              }
            });
            updateCartBadge(data);
          });
        }).catch(() => {}));
      }

      return promise;
    };

    // ── Helpers ────────────────────────────────────────────────────────────

    function restoreButton(btn, originalHTML, originalDisabled) {
      if (btn._safetyRestore) clearTimeout(btn._safetyRestore);
      btn.innerHTML = originalHTML;
      btn.disabled = originalDisabled || false;
      btn.style.opacity = '';
      btn._originalHTML = null;
    }

    /**
     * Updates ONLY the cart count badge element (not the button).
     * Looks for common badge selectors — adjust to match your template.
     */
    function updateCartBadge(data) {
      if (!data) return;
      const count = data.cart_count ?? data.quantity ?? null;
      if (count === null) return;

      // Common selectors for cart count badges — add yours if different
      const badgeSelectors = [
        '.cart-count',
        '.cart-badge',
        '#cart-count',
        '#cart-badge',
        '[data-cart-count]',
        '.navbar .badge',
      ];

      badgeSelectors.forEach(sel => {
        document.querySelectorAll(sel).forEach(el => {
          el.textContent = count;
          if (count > 0) el.style.display = '';
          else el.style.display = 'none';
        });
      });
    }

  });
})();

