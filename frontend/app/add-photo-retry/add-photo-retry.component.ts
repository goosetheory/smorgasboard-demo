import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

import { Board } from '../dtos/Board';
import { UploadUrlService } from '../services/upload-url.service';

@Component({
	selector: 'app-add-photo-retry',
	templateUrl: './add-photo-retry.component.html',
	styleUrls: ['./add-photo-retry.component.scss']
})
export class AddPhotoRetryComponent implements OnInit {
	@Output() retrySuccessful = new EventEmitter<string>();
	@Input() board: Board;
	@Input() file: any;

	private initialRetryButtonText = 'Retry?';

	retryEnabled: boolean = true;
	retrying: boolean = false;
	retryButtonText = this.initialRetryButtonText;

	constructor(private uploadService: UploadUrlService) { }

	ngOnInit(): void {
	}

	retry() {
		this.retrying = true;
		this.retryEnabled = false;
		this.retryButtonText = "Retrying...";

		if (!this.file) {
			this.retryButtonText = "No file to retry.";
			this.delayedButtonReset();
			return;
		}

		this.uploadService.uploadFile(this.file, this.board.joinCode)
		.then(response => {
			this.retrying = false;
			this.retryButtonText = 'Success!';

			this.delayedButtonReset();
			this.delayedFadeOut();
		})
		.catch(error => {
			this.retrying = false;
			this.retryButtonText = 'Retry failed.';

			this.delayedButtonReset();
		});
	}

	private delayedButtonReset() {
		setTimeout(() => {
			this.retryButtonText = this.initialRetryButtonText;
			this.retryEnabled = true;
		}, 1500);
	}

	private delayedFadeOut() {
		setTimeout(() => {
			this.retrySuccessful.emit();
		}, 1500);
	}
}
