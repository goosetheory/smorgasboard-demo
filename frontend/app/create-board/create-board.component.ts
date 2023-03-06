import { Component, OnInit, ViewChild, ElementRef, ChangeDetectorRef, HostListener } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder } from '@angular/forms';
import { Title } from '@angular/platform-browser';

import { BoardCreatedModalComponent } from '../board-created-modal/board-created-modal.component';
import { BoardService } from '../services/board.service';
import { ToastService } from '../services/toast.service';
import { PaymentService } from '../services/payment.service';

import { Board } from '../dtos/Board';
import { BoardToCreate } from '../dtos/BoardToCreate';
import { BoardType } from '../dtos/BoardType';

@Component({
	selector: 'app-create-board',
	templateUrl: './create-board.component.html',
	styleUrls: ['./create-board.component.scss']
})
export class CreateBoardComponent implements OnInit {
	@ViewChild(BoardCreatedModalComponent) boardCreatedModal: BoardCreatedModalComponent;
	@ViewChild(BoardCreatedModalComponent) freeTrialCreatedModal: BoardCreatedModalComponent;

	private readonly PaymentCheckDelayMs: number = 3000;
	bannerText: string = 'Create your Board';
	createdBoard: Board;

	canCreateBoard: boolean = false;
	remainingPaymentChecks: number = 5;

	boardCreationFormSubmitted: boolean = false;
	sampleNames = [
	'Romeo and Juliet\'s Wedding',
	'Eastside High School Prom',
	'Adam\'s Bar Mitzvah',
	'Happily Ever After',
	'Jeanie\'s Bachelorette Party',
	'Happy Birthday Abby!'
	];

	boardToCreate: BoardToCreate;

	constructor(private boardService: BoardService,
	            private titleService: Title,
	            private formBuilder: FormBuilder,
	            private router: Router,
	            private route: ActivatedRoute,
	            private toastService: ToastService,
	            private paymentService: PaymentService) { }

	ngOnInit(): void {
		var boardType = parseInt(this.route.snapshot.queryParams.boardType) as BoardType || BoardType.Standard;

		if (!Object.values(BoardType).includes(boardType)) {
			boardType = BoardType.Standard;
		}

		this.boardToCreate = {
			boardName: '',
			boardType: boardType
		};

		switch (+this.boardToCreate.boardType) {
			case BoardType.Standard:
				this.titleService.setTitle('Create your Board | SmorgasBoard');
				this.schedulePaymentCheck();
				break;
			case BoardType.FreeTrial:
				this.titleService.setTitle('Free Trial: Create your Board | SmorgasBoard');
				this.bannerText = 'Start your Free Trial';
				this.boardToCreate.boardName = 'My Free Trial Board';
				this.canCreateBoard = true;
				break;
			default:
				console.error('Could not find board type.');
				break;
		}
	}

	schedulePaymentCheck() {
		// We don't want to show board creation screen unless we're
		// pretty sure a create-board call would succeed. This verifies the
		// user has made a successful payment.
		setTimeout(() => {
			this.remainingPaymentChecks--;
			this.paymentService.getSuccessfulPayments()
			.then(payments => {
				if (payments.length) {
					this.canCreateBoard = true;
				} else if (this.remainingPaymentChecks > 0) {
					this.schedulePaymentCheck();
				}
			})
			.catch(err => {
				console.log(err);
				this.toastService.error('Could not load payment info.');
			})
		},
		this.PaymentCheckDelayMs);
	}

	createBoard(): void {
		this.boardCreationFormSubmitted = true;
		if (!this.isBoardCreationFormValid()) {
			return;
		}

		this.boardService.createBoard(this.boardToCreate)
		.then(createdBoard => {
			this.createdBoard = createdBoard;

			// Why two modal callbacks?
			// One for modal dismiss, one for clicking non-existent save button.
			this.boardCreatedModal.showModal()
			.then(
			      result => this.onBoardCreatedModalClose(createdBoard),
			      reason => this.onBoardCreatedModalClose(createdBoard));

		})
		.catch(err => {
			this.toastService.error('Unable to create board. Please contact support.');
		})
	}

	private onBoardCreatedModalClose(createdBoard: Board) {
		this.router.navigate(['board', createdBoard.joinCode]);
	}

	private isBoardCreationFormValid(): boolean {
		let name = this.boardToCreate.boardName;
		if (name.length < 4 || name.length > 64) {
			return false;
		}

		return true;
	}
}
