import { Injectable } from '@angular/core';

@Injectable({
	providedIn: 'root'
})
export class PhotoLocationService {
	private readonly baseGridColumns = 5;
	private readonly baseGridRows = 3;
	private readonly windowGridRows = this.baseGridRows - 1;
	private readonly windowGridColumns = this.baseGridColumns - 1;
	private readonly xWigglePct = 2;
	private readonly yWigglePct = 2;

	private readonly baseGridBlockedLocations: Set<number> = this.getBlockedLocations();

	private onBaseGrid = true; // If not on base grid, then on window grid
	private nextLocations = [];


	constructor() {
		this.nextLocations = this.generateShuffledArrayForGrid(this.onBaseGrid);
	}

	getNextLocation(): CanvasLocation {
		if (!this.nextLocations.length) {
			this.switchGrids();
		}

		let numRows = this.onBaseGrid ? this.baseGridRows : this.windowGridRows;
		let numColumns = this.onBaseGrid ? this.baseGridColumns : this.windowGridColumns;
		let block = this.nextLocations.pop();
		let row = block % numRows;
		let column = Math.floor(block / numRows);

		let horizOffsetPct;
		let vertOffsetPct;
		let horizWigglePct = PhotoLocationService.randNum(-this.xWigglePct, this.xWigglePct);
		let vertWigglePct = PhotoLocationService.randNum(-this.yWigglePct, this.yWigglePct);
		if (this.onBaseGrid) {
			horizOffsetPct = (100 * column / numColumns) + horizWigglePct;
			vertOffsetPct = (100 * row / numRows) + vertWigglePct;
		} else {
			let baseHoriz = 1 / (2 * this.windowGridColumns);
			let baseVert = 1 / (2 * this.windowGridRows);
			horizOffsetPct = 100 * (baseHoriz + column / this.baseGridColumns) + horizWigglePct;
			vertOffsetPct = 100 * (baseVert + row / this.baseGridRows) + vertWigglePct;
		}

		return {
			'horizOffsetPct': horizOffsetPct,
			'vertOffsetPct': vertOffsetPct
		};
	}

	private switchGrids() {
		this.onBaseGrid = !this.onBaseGrid;
		this.nextLocations = this.generateShuffledArrayForGrid(this.onBaseGrid);
	}

	private generateShuffledArrayForGrid(isBaseGrid: boolean): number[] {
		let result;
		if (!isBaseGrid) {
			result = PhotoLocationService.generateShuffledArray(this.windowGridRows * this.windowGridColumns);
		} else {
			result = PhotoLocationService.generateShuffledArray(this.baseGridRows * this.baseGridColumns);
			this.baseGridBlockedLocations.forEach(blockedLocation => {
				let index = result.indexOf(blockedLocation);
				if (index > -1) {
					result.splice(index, 1);
				}
			})
		}

		return result;
	}

	private static generateShuffledArray(size: number): number[] {
		let result = [];

		// [0, 1, 2...]
		for (let i = 0; i < size; i++) {
			result[i] = i;
		}

		// Shuffle
		for (let i = result.length - 1; i > 0; i--) {
			var rand = Math.floor(Math.random() * (i + 1));
			[result[i], result[rand]] = [result[rand], result[i]];
		}

		return result;
	}

	private static randNum(min: number, max: number): number {
		return min + (max - min) * Math.random();
	}

	private getBlockedLocations(): Set<number> {
		// Only need to block behind QR code, which is in the last slot of the first column.
		let qrCodeLocation = this.baseGridRows - 1;
		return new Set([qrCodeLocation]);
	}
}

export interface CanvasLocation {
	horizOffsetPct: number;
	vertOffsetPct: number;
}
