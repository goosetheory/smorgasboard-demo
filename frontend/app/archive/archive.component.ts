import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Title } from '@angular/platform-browser';

import { BoardService } from '../services/board.service';
import { ArchiveService } from '../services/archive.service';

import { Board } from '../dtos/Board';
import { Archive } from '../dtos/Archive';
@Component({
	selector: 'app-archive',
	templateUrl: './archive.component.html',
	styleUrls: ['./archive.component.scss']
})
export class ArchiveComponent implements OnInit {
	private joinCode: string;
	finishedLoading: boolean = false;
	board: Board = null;
	archive: Archive = null;

	constructor(private route: ActivatedRoute,
				private titleService: Title,
				private boardService: BoardService,
				private archiveService: ArchiveService) {
		this.joinCode = this.route.snapshot.params.boardID;
	}

	ngOnInit(): void {
		this.titleService.setTitle('Download Photos | SmorgasBoard');
		this.boardService.getBoardByJoinCode(this.joinCode)
		.then(board => {
			this.board = board;
			this.finishedLoading = true;
		})
		.catch(err => {
			console.error(err);
			this.finishedLoading = true;
		});

		this.archiveService.getArchiveByJoinCode(this.joinCode)
		.then(archive => {
			console.log(archive);
			this.archive = archive;
		})
		.catch(err => {
			console.error(err);
		});
	}

}
