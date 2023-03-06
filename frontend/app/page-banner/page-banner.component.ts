import { Component, OnInit, Input } from '@angular/core';

@Component({
	selector: 'app-page-banner',
	templateUrl: './page-banner.component.html',
	styleUrls: ['./page-banner.component.scss']
})
export class PageBannerComponent implements OnInit {
	@Input() bannerText: string;
	@Input() photoSrc: string;
	@Input() photoSrcAbsolute: string;

	bgImageStyle: string;
	constructor() { }

	ngOnInit(): void {
		let photoFullUrl;
		if (this.photoSrc) {
			photoFullUrl = `\"../../assets/${this.photoSrc}\"`;
		} else if (this.photoSrcAbsolute) {
			photoFullUrl = this.photoSrcAbsolute;
		}

		this.bgImageStyle = `linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url(${photoFullUrl})`
	}
}