import { Component, OnInit } from '@angular/core';

@Component({
	selector: 'app-homepage-uses',
	templateUrl: './homepage-uses.component.html',
	styleUrls: ['./homepage-uses.component.scss']
})
export class HomepageUsesComponent implements OnInit {
	public uses: String[] = [
		'weddings',
		'birthday parties',
		'bar & bat mitzvahs',
		'holiday celebrations',
		'mixers',
		'bachelorette parties',
		'quinceañeras',
		'corporate events',
		'baby showers',
	];
	constructor() { }

	ngOnInit(): void {
	}
}
