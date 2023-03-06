import { Injectable } from '@angular/core';
import { Meta } from '@angular/platform-browser';

@Injectable({
	providedIn: 'root'
})
export class SeoService {
	constructor(private metaService: Meta) { }

	public setMetaDescription(str: string) {
		var span = document.createElement('span');
		span.innerHTML = str;
		let escapedStr = span.textContent || span.innerText;
		console.log(escapedStr);
		this.metaService.updateTag({ name: 'description', content: escapedStr});
	}
}
