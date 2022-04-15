// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) requestIdtoSender;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event tokenIdToBreedAssigned(
        uint256 indexed tokenID,
        Breed breed,
        address requester
    );

    constructor(
        address _VRFCoordinator,
        address _linkToken,
        bytes32 _keyhash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_VRFCoordinator, _linkToken)
        ERC721("Doggie", "Dog")
    {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdtoSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
        return requestId;
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Breed breed = Breed(randomNumber % 3);
        uint256 tokenId = tokenCounter;
        tokenIdToBreed[tokenId] = breed;
        emit tokenIdToBreedAssigned(tokenId, breed, msg.sender);
        _safeMint(requestIdtoSender[requestId], tokenId); //burda msg.sender VRFCoordinator oldugu için önce maplicez
        //_setTokenURI(newTokenId, tokenURI);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenUri(uint256 _tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), _tokenId),
            "ERC721: transfer caller is not owner nor approved"
        );
        _setTokenURI(_tokenId, _tokenURI);
    }
}
