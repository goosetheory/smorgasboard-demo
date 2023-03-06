import { Component, Input, OnInit } from '@angular/core';
import { trigger, state, style, animate, transition } from '@angular/animations';

import { Photo } from '../../dtos/photo';
import { PhotoLocationService } from '../../services/photo-location.service';

@Component({
	selector: 'app-board-photo',
	templateUrl: './board-photo.component.html',
	styleUrls: ['./board-photo.component.scss'],
	animations: [
		trigger('imageLoaded', [
			state('notLoaded', style({ opacity: 0 })),
			state('loaded', style({ opacity: 1 })),
			transition('notLoaded => loaded', [
				animate('1s ease-in-out')
			])
		]),
	]
})

export class BoardPhotoComponent implements OnInit {
	@Input() photo: Photo;
	@Input() photoIndex: number;
	style: object;
	imageLoaded: boolean = false;

	constructor(private photoLocationService: PhotoLocationService) { }

	ngOnInit(): void {
		this.style = this.getStyle();
	}

	onImageLoad(): void {
		this.imageLoaded = true;
	}

	private getStyle(): object {
		let maxWidthPct = 24;
		let maxHeightPct = 38;
		let maxRotationDegrees = 15;

		let rotateDegrees = this.randInt(-maxRotationDegrees, maxRotationDegrees);
		let nextLocation = this.photoLocationService.getNextLocation();

		return {
			'transform': 'rotate(' + rotateDegrees + 'deg)',
			'max-width': maxWidthPct + '%',
			'max-height': maxHeightPct + '%',
			'left': nextLocation.horizOffsetPct + '%',
			'top': nextLocation.vertOffsetPct + '%'
		};
	}

	private randInt(min: number, max: number) : number {
		min = Math.ceil(min);
		max = Math.floor(max);
		return Math.round((max - min) * Math.random() + min);
	}
}
