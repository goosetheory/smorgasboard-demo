import { PaymentStatus } from './PaymentStatus';

export class Payment {
	paymentDate: Date;
	constructor(public paymentStatus: PaymentStatus,
	            public paymentDateTimestamp: number,
	            public stripePaymentId: string,
	            public amount: number) {
		this.paymentDate = new Date(paymentDateTimestamp)
	}


	static fromWire(wire) {
		return new Payment(wire.paymentStatus,
		                   wire.paymenetDateTimestamp,
		                   wire.stripePaymentId,
		                   wire.amount);
	}
}