import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Title } from '@angular/platform-browser';

import { Board } from '../dtos/Board';
import { BoardStatus } from '../dtos/BoardStatus';
import { UploadUrlService } from '../services/upload-url.service';
import { BoardService } from '../services/board.service';

@Component({
	selector: 'app-add-photo',
	templateUrl: './add-photo.component.html',
	styleUrls: ['./add-photo.component.scss']
})
export class AddPhotoComponent implements OnInit {
	private initialUploadButtonText = 'Take a Photo';

	finishedLoading: boolean = false;
	boardJoinCode: string;
	board: Board;
	uploading: boolean;
	uploadEnabled = true;
	uploadButtonText = this.initialUploadButtonText;
	failedFile: any;

	constructor(private route: ActivatedRoute,
	            private titleService: Title,
				private uploadService: UploadUrlService,
				private boardService: BoardService) { }

	ngOnInit(): void {
		this.titleService.setTitle('Add a Photo | SmorgasBoard');
		this.boardJoinCode = this.route.snapshot.params.boardID;
		this.boardService.getBoardByJoinCode(this.boardJoinCode)
		.then(board => {
			this.board = board;
			this.finishedLoading = true;
		})
		.catch(err => {
			console.error(err);
			this.finishedLoading = true;
		});
	}

	onPhotoChange(event) {
		let selectedFiles = event.target.files;
		this.failedFile = null;
		if (selectedFiles) {
			this.uploading = true;
			this.uploadEnabled = false;
			this.uploadButtonText = 'Uploading...';

			let file = event.target.files[0];
			this.uploadService.uploadFile(file, this.boardJoinCode)
			.then(response => {
				this.uploadButtonText = 'Success!';
			})
			.catch(error => {
				this.uploadButtonText = 'Upload failed.';
				this.failedFile = file;

				console.error(error);
			})
			.finally(() => {
				this.uploading = false;
				this.delayedButtonReset();
			});
		}
		else {
			return Promise.resolve(null);
		}
	}

	public canUpload() {
		return this.board && this.board.boardStatus == BoardStatus.Active;
	}

	onRetrySuccessful(event) {
		this.failedFile = null;
	}

	private delayedButtonReset() {
		setTimeout(() => {
					this.uploadButtonText = this.initialUploadButtonText;
					this.uploadEnabled = true;
				}, 1500);
	}
}
