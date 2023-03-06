import { Injectable, TemplateRef } from '@angular/core';

@Injectable({
	providedIn: 'root'
})
export class ToastService {
	public toasts: any[] = [];

	constructor() { }

	// Push new Toasts to array with content and options
	show(text: string) {
		let options = {
			delay: 10000,
			autohide: true,
		};
		this.toasts.push({text, ...options});
	}

	error(text: string) {
		let options = {
			delay: 10000,
			autohide: true,
			classname: 'bg-danger text-light'
		};
		this.toasts.push({text, ...options});
	}

	// Callback method to remove Toast DOM element from view
	remove(toast) {
		this.toasts = this.toasts.filter(t => t !== toast);
	}
}
