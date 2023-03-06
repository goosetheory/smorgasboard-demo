import { Injectable } from '@angular/core';

@Injectable({
	providedIn: 'root'
})
export class AddPhotoLinkService {
	basePath: string;
	relativePath: string = 'add-photo/'
	localIP: string = 'http://192.168.2.113:4200'

	constructor() {
		if (window.location.origin.includes('localhost')) {
			this.basePath = this.localIP
		} else {
			this.basePath = window.location.origin;
		}
	}

	public getAddPhotoLink(joinCode: string): string {
		return this.basePath + '/' + this.relativePath + joinCode;
	}
}
