import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';


import { BoardService } from '../services/board.service';
import { BoardMembershipService } from '../services/board-membership.service';
import { Board } from '../dtos/Board';
import { BoardMembership } from '../dtos/BoardMembership';

@Component({
	selector: 'app-join-board',
	templateUrl: './join-board.component.html',
	styleUrls: ['./join-board.component.scss']
})
export class JoinBoardComponent implements OnInit {
	private readonly initialJoinButtonText = 'Join!';
	boardJoinCode: string;

	board: Board;
	currentMembership: BoardMembership;

	canJoinBoard: boolean = false;
	joiningBoard: boolean = false;
	joinButtonText: string = this.initialJoinButtonText;
	joinButtonEnabled: boolean = true;

	boardDoesNotExist: boolean = false;
	get alreadyMember() {
		return this.board &&
		this.currentMembership &&
		this.board.joinCode == this.currentMembership.joinCode;
	}

	constructor(private route: ActivatedRoute,
	            private router: Router,
	            private boardService: BoardService,
	            private boardMembershipService: BoardMembershipService) { }

	ngOnInit(): void {
		this.boardJoinCode = this.route.snapshot.params['boardID'];
		this.boardService.getBoardByJoinCode(this.boardJoinCode)
		.then(board => {
			this.board = board;
			if (!board) {
				this.boardDoesNotExist = true;
			} else {
				this.boardMembershipService.getBoardMemberships()
				.then(response => {
					if (response.length > 0) {
						this.currentMembership = response[0];
					}

					if (!this.alreadyMember) {
						this.canJoinBoard = true;
					}
				});
			}
		})
		.catch(error => {
			console.error(error);
		});
	}

	joinBoard(): void {
		this.joiningBoard = true;
		this.joinButtonEnabled = false;
		this.joinButtonText = 'Joining...'

		this.boardMembershipService.joinBoard(this.board.joinCode)
		.then(response => {
			this.joiningBoard = false;
			this.joinButtonText = 'Success!';

			setTimeout(() => {
				this.router.navigate(['']);
			}, 1500);
		})
		.catch(error => {
			console.error(error);

			this.joiningBoard = false;
			this.joinButtonText = 'Failed to Join.';

			setTimeout(() => {
				this.joinButtonText = this.initialJoinButtonText;
				this.joinButtonEnabled = true;
			}, 1500);
		})
	}
}
