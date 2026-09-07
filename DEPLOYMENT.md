# Deployment

Network: GenLayer StudioNet, chain ID `61999`.

| Contract | Address | Finalized deployment transaction |
| --- | --- | --- |
| Errata | `0x42Fc7737C8A3750918a7996853d8E81052A62109` | `0x41131db426dd87bd13035d46f9024610ffbdb8ec201671fc910a04081fba549c` |
| CanonGate (configured for the Errata address above) | `0xE06548440448B24b946f7aFc2A26F62140f31870` | `0x085d6d5f5b2ab663478d6e950c49c1f232cdf7f1b74280f9014f49eb7d639d3c` |

Both receipts were verified as `FINALIZED`, `SUCCESS`, and `MAJORITY_AGREE`.

Initial lifecycle transactions:

- `create_record`: `0xcf2e7e44ef6149f58b1c07226f42e2149123da3969f0706f68f6ec7e5d8c5339`
- `add_authority_host`: `0xbc190087393d21f9a9dc94633cab814722ac653ef14139ff0fc681f732bc16e1`
- `publish_initial`: `0x1cff6e36532faaa44c4642d5f6e9596821f24ec0e08e59f61e59538d89433e68`
- `create_claim`: `0x53f4e26f916ac264a5c95f11862822da8a24ca68fd4348768cfcbc15c9bfc1c3`
- first current `CanonGate.execute_if_current`: `0x0e2c8c268eb54b9d1ca39ca0d35340b4797492fbe92acfdd14ff920a0697b7e7`
- confirmation `propose_revision` (CONFIRMS): `0x9f6a8ceb012176b68fe203b18c04419b4bdc0d062a66abe3f9f49f707c3a7aa3`
- second current `CanonGate.execute_if_current`: `0x799c40a5ddf828287de8a6e30252f3c4be761b1ea3ac46e41d44415f5dc4f3c5`
- correction `propose_revision` (material): `0x39147707ac6c8ff9ea7745b4ec0fe29391f7213f195673f73fdc3bb6f34fe753`
- stale-claim `CanonGate.execute_if_current` rejection: `0x52cae4871efdf50780b6f3ff9a90bd4782cc3d079c5362ea2edf0bf0a0ff4bb3`
- fresh claim pinned to revision 3: `0x46f2b29ce1aa576f41f50d1d6f47e8aaed7ce3dd0ed16192b393f4701e5ceb6d`
- final current `CanonGate.execute_if_current`: `0x62cff49ae37e41c0b119d241ef9fae4b563d0a443ddc47a679f268de9d2e9a60`

Every lifecycle receipt above was independently polled to `FINALIZED`; successful transactions returned `SUCCESS` and `MAJORITY_AGREE`. The stale-claim rejection also finalized with `MAJORITY_AGREE` and contract execution `ERROR`, as expected.
