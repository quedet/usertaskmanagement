import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
    static targets = ['submit'];

    disconnect() {
        this.enableSubmits();
        this.element.toggleAttribute("data-submitting", false);
    }

    enableSubmits() {
        this.submitTargets.forEach(submitTarget => {
            submitTarget.disabled = false;
        });
    }

    disableSubmits() {
        this.submitTargets.forEach(submitTarget => {
            submitTarget.disabled = true;
        });
    }

    submitStart() {
        const form = this.element;
        if (form) {
            form.toggleAttribute("data-submitting", true);
            this.disableSubmits();
        }
    }

    submitEnd() {
        const form = this.element;
        if (form) {
            form.toggleAttribute("data-submitting", false);
            this.enableSubmits();
        }
    }
}