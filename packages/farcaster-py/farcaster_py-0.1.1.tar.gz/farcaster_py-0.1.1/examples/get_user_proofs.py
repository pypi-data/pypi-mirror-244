import os
import sys
from dotenv import load_dotenv
from farcaster.HubService import HubService

load_dotenv()
hub_address	= os.getenv("FARCASTER_HUB")
if not hub_address:
	print("No hub address. Check .env.sample")
	sys.exit(1)

hub = HubService(hub_address, use_async=False)
proofs = hub.GetUserNameProofsByFid(fid=19150)
print(proofs)
for proof in proofs.proofs:
	print(proof)
