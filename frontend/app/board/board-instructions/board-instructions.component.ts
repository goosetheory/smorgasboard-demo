import { Input, Component, OnInit } from '@angular/core';
import { AddPhotoLinkService } from '../../services/add-photo-link.service';
import { ToastService } from '../../services/toast.service';

import { Board } from '../../dtos/Board';
import { BoardType } from '../../dtos/BoardType';

@Component({
	selector: 'app-board-instructions',
	templateUrl: './board-instructions.component.html',
	styleUrls: ['./board-instructions.component.scss']
})
export class BoardInstructionsComponent implements OnInit {
	@Input() board: Board;
	public addPhotoLink: string;
	constructor(private addPhotoLinkService: AddPhotoLinkService,
	            private toastService: ToastService) { }

	ngOnInit(): void {
		this.addPhotoLink = this.addPhotoLinkService.getAddPhotoLink(this.board.joinCode);
	}

	isFreeTrial(): boolean {
		return this.board && this.board.boardType == BoardType.FreeTrial;
	}

	public copyLink() {
		navigator.clipboard.writeText(this.addPhotoLink)
		.then(_ => {
			this.toastService.show("Link copied to clipboard.");
		})
		.catch(e => console.error(e));
	}
}
