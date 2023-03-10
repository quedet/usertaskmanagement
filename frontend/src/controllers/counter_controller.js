import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  static values = {
    count: {
      type: Number, default: 0
    }
  };

  static targets = ['count', 'initial', 'progress'];

  static classes = ['hidden', 'btnOutlineRed', 'btnRed', 'btnOutlineBlue'];

  connect() {
    this.countTarget.innerHTML = this.countValue;
  }

  countValueChanged(value,) {
    if (value == 1) {
      this.initialTarget.classList.add(this.hiddenClass);
      this.progressTarget.classList.remove(this.hiddenClass);
    }
  }

  increment() {
    this.countValue++;
    this.countTarget.innerHTML = this.countValue;

    if (this.countValue >= 5) {
      this.element.classList.remove(this.btnOutlineBlueClass);
      this.element.classList.add(this.btnClass);
    }

    if (this.countValue >= 10) {
      this.element.classList.remove(this.btnClass);
      this.element.classList.add(this.btnRedClass);
    }
  }
}
