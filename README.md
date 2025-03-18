# RL-agent-parser [Lagrange I]
Experimental Basic RL-agent Parser for IBKR Fills, fitted on A2C, PPO, TD3, SAC.

Agent is trained to make 'best' trades for the given models and data
- Market Orders
- Stop Loss Limits
- Long / Short or No Actions

Custom Reward Function based on 
- philosophical dilemmas
  * Temporal Paradox
  * Overcrowded Lifeboat
  * Newcomb’s Paradox
  * Lottery Paradox
  * Liar’s Paradox
- inactivity penalization
- Cumulative Returns
- Instant vs Delayed Gratification

Environment comprises on revelant sentiment/volatility/models with both static and dynamic observations

Instead of truncating episodes at 20-30% drawdowns / High Water Mark thresholds which do not allow the agent to learn anything of substance,
Episode termination/truncation is set done when A/C balance raeches 0
