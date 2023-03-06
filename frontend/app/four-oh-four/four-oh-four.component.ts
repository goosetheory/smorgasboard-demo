import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';

@Component({
	selector: 'app-four-oh-four',
	templateUrl: './four-oh-four.component.html',
	styleUrls: ['./four-oh-four.component.scss']
})
export class FourOhFourComponent implements OnInit {

	constructor(private titleService: Title) { }

	ngOnInit(): void {
		this.titleService.setTitle('404 | SmorgasBoard');
	}

}
