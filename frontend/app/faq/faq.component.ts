import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';

@Component({
	selector: 'app-faq',
	templateUrl: './faq.component.html',
	styleUrls: ['./faq.component.scss']
})
export class FaqComponent implements OnInit {

	constructor(private titleService: Title) { }

	ngOnInit(): void {
		this.titleService.setTitle('Frequently Asked Questions | SmorgasBoard');
	}

}
