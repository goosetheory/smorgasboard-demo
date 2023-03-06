import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';

@Component({
	selector: 'app-cookies-policy',
	templateUrl: './cookies-policy.component.html',
	styleUrls: ['./cookies-policy.component.scss']
})
export class CookiesPolicyComponent implements OnInit {

	constructor(private titleService: Title) { }

	ngOnInit(): void {
		this.titleService.setTitle('Cookies Policy | SmorgasBoard');
	}
}
