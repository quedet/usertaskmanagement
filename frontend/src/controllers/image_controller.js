import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
    static targets = ['profile', 'current'];

    handlePreview() {
        this.profileTarget.setAttribute("src", this.currentTarget);
        this.element.setAttribute("src", "");
    }
}