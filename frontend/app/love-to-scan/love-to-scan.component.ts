import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';

@Component({
	selector: 'app-love-to-scan',
	templateUrl: './love-to-scan.component.html',
	styleUrls: ['./love-to-scan.component.scss']
})
export class LoveToScanComponent implements OnInit {

	constructor(private titleService: Title) { }

	ngOnInit(): void {
		this.titleService.setTitle('Nice Scan! | SmorgasBoard');
	}

}
