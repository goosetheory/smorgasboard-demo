import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Title } from '@angular/platform-browser';

import { UploadUrlService } from '../services/upload-url.service';
import { BoardService } from '../services/board.service';
import { Board } from '../dtos/Board';
import { Photo } from '../dtos/Photo';
import { BoardStatus } from '../dtos/BoardStatus';
import { BoardPhotoStatus } from '../dtos/BoardPhotoStatus';
import { PhotoModalComponent } from './photo-modal/photo-modal.component';

@Component({
	selector: 'app-all-photos',
	templateUrl: './all-photos.component.html',
	styleUrls: ['./all-photos.component.scss']
})
export class AllPhotosComponent implements OnInit {
	@ViewChild(PhotoModalComponent) photoModal: PhotoModalComponent;

	photos = [];
	noMorePhotos: boolean = false;
	board: Board;
	linkToBoard: string;
	boardCompleted: boolean = false;

	private readonly joinCode: string;
	private nextPage: number = 0;
	readonly pageSize = 6;

	readonly beforeDate;
	readonly numColumns = 3;

	constructor(private route: ActivatedRoute,
	            private uploadUrlService: UploadUrlService,
	            private boardService: BoardService,
	            private titleService: Title) {
		this.joinCode = this.route.snapshot.params.boardID;
		this.beforeDate = new Date();
	}

	ngOnInit(): void {
		this.linkToBoard = `/board/${this.joinCode}`

		this.titleService.setTitle('Manage Photos | SmorgasBoard');

		if (this.joinCode) {
			this.boardService.getBoardByJoinCode(this.joinCode)
			.then(board => {
				this.board = board;
				if (this.board.boardStatus == BoardStatus.Completed) {
					this.boardCompleted = true;
				} else {
					this.getNextPage();
				}
			})
			.catch(err => {
				console.log(err);
			})
		} else {
			console.warn('No join code provided in url: ' + window.location.href);
		}
	}

	getNextPage(): void {
		if (this.noMorePhotos) {
			return;
		}

		let photoStatuses = [BoardPhotoStatus.Active, BoardPhotoStatus.RemovedByHost];

		this.uploadUrlService.getPhotoUrls(this.joinCode, photoStatuses, this.beforeDate, this.nextPage, this.pageSize)
		.then(response => {
			if (!response || !response.length) {
				this.noMorePhotos = true;
			}
			this.photos.push(...response);
		});

		this.nextPage++;
	}

	onPhotoClick(photo: Photo) {
		this.photoModal.showModal(photo)
		.then(
			result => {
				photo.boardPhotoStatus = BoardPhotoStatus.RemovedByHost;
			},
			reason => {})
	}

	range(start: number, size: number): number[] {
		return Array(size).fill(0).map((x, i) => start + i);
	}
}
