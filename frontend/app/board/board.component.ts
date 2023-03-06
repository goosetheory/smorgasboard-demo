import { Component, OnInit, ViewChild, ElementRef, ChangeDetectorRef, HostListener } from '@angular/core';
import { API, Auth } from 'aws-amplify';
import { Router, ActivatedRoute } from '@angular/router';
import { Title } from '@angular/platform-browser';

import { BoardStartModalComponent } from './board-start-modal/board-start-modal.component';
import { BoardService } from '../services/board.service';
import { UploadUrlService } from '../services/upload-url.service';

import { Board } from '../dtos/Board';
import { Photo } from '../dtos/Photo';

@Component({
	selector: 'app-board',
	templateUrl: './board.component.html',
	styleUrls: ['./board.component.scss']
})
export class BoardComponent implements OnInit {
	@ViewChild(BoardStartModalComponent) boardStartModal: BoardStartModalComponent;
	joinCode: string = null;
	board: Board = null;
	allPhotosLink: string;

	constructor(private route: ActivatedRoute,
	            private boardService: BoardService,
	            private titleService: Title,
	            private router: Router) { }

	ngOnInit(): void {
		this.titleService.setTitle('Board | SmorgasBoard');

		this.joinCode = this.route.snapshot.params.boardID;

		this.allPhotosLink = `/board/${this.joinCode}/manage-photos`

		if (this.joinCode) {
			this.boardService.getBoardByJoinCode(this.joinCode)
			.then(board => {
				this.board = board;
			})
			.catch(err => {
				console.log(err);
				// TODO(sgoldstein)
			})
		} else {
			console.warn('No join code provided in url: ' + window.location.href);
			this.router.navigate(['boards']);
		}
	}

	startBoard(): void {
		this.boardStartModal.showModal()
		.then(
				result => this.onStartBoardModalAccepted(),
				reason => {});
	}

	private onStartBoardModalAccepted() {
		return this.boardService.startBoard(this.board.joinCode)
		.then(result => {
			this.board = result;
		});
	}

}
