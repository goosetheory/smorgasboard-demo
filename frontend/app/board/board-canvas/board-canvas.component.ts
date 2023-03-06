import { Input, Output, Component, OnInit, OnDestroy, ViewChild, NgZone, ElementRef, ChangeDetectorRef, HostListener, EventEmitter } from '@angular/core';
import { trigger, state, style, animate, transition } from '@angular/animations';

import { PhotoCanvasService } from '../../services/photo-canvas.service';
import { CanvasAlertComponent } from '../canvas-alert/canvas-alert.component';
import { Board } from '../../dtos/Board';
import { BoardStatus } from '../../dtos/BoardStatus';
import { Photo } from '../../dtos/Photo';

import { map } from 'rxjs/operators';

@Component({
	selector: 'app-board-canvas',
	templateUrl: './board-canvas.component.html',
	styleUrls: ['./board-canvas.component.scss'],
	animations: [
	trigger('removeTrigger', [
	        transition(':leave', [
	                   animate('1s ease-in-out', style({ opacity: 0 }))
	                   ]
	                   )])
	]
})
export class BoardCanvasComponent implements OnInit, OnDestroy {
	@Input() board: Board;
	@Output() startBoardCall = new EventEmitter();

	@ViewChild('photoCanvas') photoCanvas: ElementRef;
	@ViewChild('canvasAlert') canvasAlert: CanvasAlertComponent;

	@HostListener('document:fullscreenchange', [])
	@HostListener('document:webkitfullscreenchange', [])
	onFullscreenChange(event) {
		this.ref.detectChanges();
	}

	loading: boolean = false;
	launched: boolean = false;

	showAlert: boolean = false;
	showConnectionError: boolean = false;
	showReconnectionMessage: boolean = false;

	constructor(public photoCanvasService: PhotoCanvasService,
	            private ref: ChangeDetectorRef,
	            private ngZone: NgZone) {
	}

	ngOnInit(): void {
		this.photoCanvasService.setTriggers(this.onDisconnect, this.onReconnect);
	}

	ngOnDestroy(): void {
		this.photoCanvasService.teardown();
	}

	startBoardForFirstTime() {
		if (this.board.boardStatus != BoardStatus.NotStarted) {
			return;
		}

		this.startBoardCall.emit();
	}

	toggleFullscreen() {
		if (!this.isFullscreen()) {
			this.enterFullscreen();
		} else {
			this.exitFullscreen();
		}
	}

	isFullscreen() {
		let doc = <any> document;
		return (!!doc.fullscreenElement
		        || !!doc.webkitCurrentFullScreenElement); /* Safari */
	}

	enterFullscreen() {
		if (!this.launched) {
			this.launch();
		}

		let canvasElt = <any> this.photoCanvas.nativeElement;
		if (canvasElt.requestFullscreen) {
			canvasElt.requestFullscreen();
		} else if (canvasElt.webkitRequestFullscreen) { /* Safari */
			canvasElt.webkitRequestFullscreen();
		}
	}

	exitFullscreen() {
		let doc = <any> document;
		if (doc.exitFullscreen) {
			doc.exitFullscreen();
		} else if (doc.webkitExitFullscreen) { /* Safari */
			doc.webkitExitFullscreen();
		}
	}

	boardIsActive() {
		return this.board.boardStatus == BoardStatus.Active;
	}

	boardIsNotStarted() {
		return this.board.boardStatus == BoardStatus.NotStarted;
	}

	boardIsCompleted() {
		return this.board.boardStatus == BoardStatus.Completed;
	}

	onDisconnect = () => {
		this.canvasAlert.onDisconnect();
	}

	onReconnect = () => {
		this.canvasAlert.onReconnect();
	}

	private launch() {
		this.launched = true;
		this.loading = true;

		this.photoCanvasService.initialize(this.board)
		.finally(() => {
			this.loading = false;
		})
	}
}
