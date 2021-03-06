/*
 * Copyright (c) ZHAW and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package ch.icclab.netfloc.iface;

public interface IServiceChainListener {
	public void serviceChainCreated(IServiceChain sc);
	//public void serviceChainUpdated(IServiceChain osc, IServiceChain nsc);
	public void serviceChainDeleted(IServiceChain sc);
}
