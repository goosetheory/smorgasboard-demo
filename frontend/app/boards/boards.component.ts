import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';

import { BoardService } from '../services/board.service';
import { PaymentService } from '../services/payment.service';

import { Board } from '../dtos/Board';

@Component({
	selector: 'app-boards',
	templateUrl: './boards.component.html',
	styleUrls: ['./boards.component.scss']
})
export class BoardsComponent implements OnInit {
	boards: Board[];
	boardsFinishedLoading: boolean = false;
	paymentsFinishedLoading: boolean = false;
	createBoardHref: string = '';

	constructor(private titleService: Title,
	            private boardService: BoardService,
	            private paymentService: PaymentService) { }

	ngOnInit(): void {
		this.titleService.setTitle('Your Boards | SmorgasBoard');

		this.paymentService.getSuccessfulPayments()
		.then(payments => {
			if (payments.length > 0) {
				// User has already made a successful, unconsumed payment.
				// Create board button should lead to create-board page.
				this.createBoardHref = "/create-board";
			} else {
				// User has no unconsumed payments. Create board button should
				// Lead to checkout page.
				this.createBoardHref = "/checkout";
			}
		})
		.catch(err => {
			console.error(err);
		})
		.finally(() => {
			this.paymentsFinishedLoading = true;
		})

		this.boardService.getBoards()
		.then(boards => {
			this.boards = boards;
			this.boardsFinishedLoading = true;
		})
		.catch(err => {
			console.error(err);
		})
		.finally(() => {
			this.paymentsFinishedLoading = true;
		});
	}

}
