import { Component, OnInit } from '@angular/core';
import { trigger, state, style, animate, transition } from '@angular/animations';
import { Title } from '@angular/platform-browser';

@Component({
	selector: 'app-contact-us',
	templateUrl: './contact-us.component.html',
	styleUrls: ['./contact-us.component.scss'],
	animations: [
		trigger('showEmail', [
			state('hide', style({ opacity: 0 })),
			state('show', style({ opacity: 1 })),
			transition('hide => show', [
				animate('1s 3s ease-in-out')
			])
		]),
	]
})
export class ContactUsComponent implements OnInit {
	showEmail: boolean = false;
	emailAddress: string = '';
	mailtoLink: string = '#';
	readonly encodedEmailAddress = 'c2FtQHNtb3JnYXNib2FyZC5pbw==';

	constructor(private titleService: Title,) { }

	ngOnInit(): void {
		this.titleService.setTitle('Contact Us | SmorgasBoard');
	}

	onClick() {
		this.showEmail = true;
		this.emailAddress = atob(this.encodedEmailAddress);
		this.mailtoLink = 'mailto:' + this.emailAddress;
	}
}
