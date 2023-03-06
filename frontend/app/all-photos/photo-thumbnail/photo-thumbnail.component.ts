import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';

import { Photo } from '../../dtos/Photo';
import { BoardPhotoStatus } from '../../dtos/BoardPhotoStatus';

@Component({
	selector: 'app-photo-thumbnail',
	templateUrl: './photo-thumbnail.component.html',
	styleUrls: ['./photo-thumbnail.component.scss']
})
export class PhotoThumbnailComponent implements OnInit {
	@Input() photo: Photo;
	@Output() onClick = new EventEmitter<Photo>();

	constructor() { }

	ngOnInit(): void {
	}

	photoClicked(): void {
		this.onClick.emit(this.photo);
	}

	photoEnabled(): boolean {
		return this.photo.boardPhotoStatus == BoardPhotoStatus.Active;
	}
}
