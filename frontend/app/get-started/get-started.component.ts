import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';

@Component({
	selector: 'app-get-started',
	templateUrl: './get-started.component.html',
	styleUrls: ['./get-started.component.scss']
})
export class GetStartedComponent implements OnInit {
	constructor(private titleService: Title) { }

	ngOnInit(): void {
		this.titleService.setTitle('Get Started | SmorgasBoard');
	}
}
