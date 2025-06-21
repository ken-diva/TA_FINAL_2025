// Handle mouse move for hover effects
function onMouseMove(event) {
	const rect = renderer.domElement.getBoundingClientRect();
	mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
	mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

	raycaster.setFromCamera(mouse, camera);
	const intersects = raycaster.intersectObjects(scene.children, true);

	// Reset cursor
	renderer.domElement.style.cursor = "default";

	// Check for building hover
	for (let i = 0; i < intersects.length; i++) {
		const object = intersects[i].object;
		if (object.userData.isBuilding) {
			renderer.domElement.style.cursor = "pointer";
			break;
		}
	}
} // 3D Map Initialization
let scene, camera, renderer, controls;
let raycaster, mouse;
let buildings = [];
let selectedBuilding = null;
let loadingIndicator;
let outlinePass, composer;

// Building codes from the model
const BUILDING_CODES = [
	"GDG-A",
	"GDG-B",
	"GDG-BAS1",
	"GDG-BAS2",
	"GDG-E",
	"GDG-F",
	"GDG-FIF",
	"GDG-FIT",
	"GDG-FKSFEBPERP",
	"GDG-FRI",
	"GDG-FTE",
	"GDG-GKU",
	"GDG-GSG",
	"GDG-JOG",
	"GDG-LING",
	"GDG-MSU",
	"GDG-PASCA",
	"GDG-PUTRA",
	"GDG-PUTRI",
	"GDG-REKT",
	"GDG-SPRT",
	"GDG-STD",
	"GDG-TUCH",
	"GDG-TULT",
];

// Building names mapping
const BUILDING_NAMES = {
	"GDG-A": "Building A",
	"GDG-B": "Building B",
	"GDG-BAS1": "Basketball Court 1",
	"GDG-BAS2": "Basketball Court 2",
	"GDG-E": "Building E",
	"GDG-F": "Building F",
	"GDG-FIF": "FIF Building",
	"GDG-FIT": "FIT Building",
	"GDG-FKSFEBPERP": "FKSF/FEB/PERP",
	"GDG-FRI": "FRI Building",
	"GDG-FTE": "FTE Building",
	"GDG-GKU": "GKU Building",
	"GDG-GSG": "GSG Building",
	"GDG-JOG": "Jogging Track",
	"GDG-LING": "Language Center",
	"GDG-MSU": "MSU Building",
	"GDG-PASCA": "Graduate Building",
	"GDG-PUTRA": "Male Dormitory",
	"GDG-PUTRI": "Female Dormitory",
	"GDG-REKT": "Rectorate Building",
	"GDG-SPRT": "Sports Complex",
	"GDG-STD": "Stadium",
	"GDG-TUCH": "TUCH Building",
	"GDG-TULT": "TULT Building",
};

// Building descriptions
const BUILDING_DESCRIPTIONS = {
	"GDG-A": "Academic Building A - General classrooms and lecture halls",
	"GDG-B": "Academic Building B - Laboratory and research facilities",
	"GDG-BAS1":
		"Indoor Basketball Court 1 - Professional court with spectator seating",
	"GDG-BAS2": "Indoor Basketball Court 2 - Training and practice facility",
	"GDG-E": "Engineering Building - Engineering departments and workshops",
	"GDG-F": "Faculty Building - Administrative offices and meeting rooms",
	"GDG-FIF": "Faculty of Informatics - Computer labs and IT facilities",
	"GDG-FIT":
		"Faculty of Industrial Technology - Engineering labs and workshops",
	"GDG-FKSFEBPERP": "Business, Communication, and Library complex",
	"GDG-FRI": "Faculty of Creative Industries - Art studios and design labs",
	"GDG-FTE":
		"Faculty of Electrical Engineering - Electronics and electrical labs",
	"GDG-GKU": "Main Auditorium - Large capacity auditorium for events",
	"GDG-GSG": "Multipurpose Hall - Sports and cultural activities",
	"GDG-JOG": "Outdoor Jogging Track - 400m athletic track",
	"GDG-LING": "Language Learning Center - Language labs and classrooms",
	"GDG-MSU": "Student Center - Student organizations and activities",
	"GDG-PASCA": "Postgraduate Building - Graduate programs and research",
	"GDG-PUTRA": "Male Student Dormitory - Accommodation for male students",
	"GDG-PUTRI": "Female Student Dormitory - Accommodation for female students",
	"GDG-REKT": "University Administration - Main administrative offices",
	"GDG-SPRT": "Main Sports Complex - Various indoor sports facilities",
	"GDG-STD": "University Stadium - Football field and athletic facilities",
	"GDG-TUCH": "University Health Center - Medical and health services",
	"GDG-TULT": "Advanced Technology Lab - Research and development center",
};

// Initialize Three.js scene
function init() {
	loadingIndicator = document.getElementById("loading-indicator");
	const container = document.getElementById("map-container");

	// Scene setup
	scene = new THREE.Scene();
	scene.background = new THREE.Color(0xf5f5f5); // Light gray background

	// Camera setup - perspective view
	camera = new THREE.PerspectiveCamera(
		75,
		container.clientWidth / container.clientHeight,
		0.01, // Smaller near plane for close-up viewing
		1000
	);
	camera.position.set(10, 10, 10);
	camera.lookAt(0, 0, 0);

	// Renderer setup
	renderer = new THREE.WebGLRenderer({
		antialias: true,
		alpha: true,
		powerPreference: "high-performance",
	});
	renderer.setSize(container.clientWidth, container.clientHeight);
	renderer.shadowMap.enabled = true;
	renderer.shadowMap.type = THREE.VSMShadowMap; // Softer, better quality shadows
	renderer.setPixelRatio(window.devicePixelRatio);
	renderer.toneMapping = THREE.ACESFilmicToneMapping;
	renderer.toneMappingExposure = 1;
	renderer.outputEncoding = THREE.sRGBEncoding;
	container.appendChild(renderer.domElement);

	// Controls setup - OrbitControls for free rotation
	controls = new THREE.OrbitControls(camera, renderer.domElement);
	controls.enableDamping = true;
	controls.dampingFactor = 0.05;
	controls.screenSpacePanning = false;
	controls.minDistance = 0.5; // Allow closer zoom
	controls.maxDistance = 50;
	controls.maxPolarAngle = Math.PI / 2;

	// Lighting setup
	setupLighting();

	// Raycaster for mouse interaction
	raycaster = new THREE.Raycaster();
	mouse = new THREE.Vector2();

	// Load 3D model
	loadGLBModel();

	// Event listeners
	window.addEventListener("resize", onWindowResize, false);
	container.addEventListener("click", onMouseClick, false);
	container.addEventListener("mousemove", onMouseMove, false);
}

// Setup lighting
function setupLighting() {
	// Ambient light for overall illumination
	const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
	scene.add(ambientLight);

	// Main directional light
	const directionalLight = new THREE.DirectionalLight(0xffffff, 0.6);
	directionalLight.position.set(10, 20, 10);
	directionalLight.castShadow = true;
	directionalLight.shadow.camera.left = -30;
	directionalLight.shadow.camera.right = 30;
	directionalLight.shadow.camera.top = 30;
	directionalLight.shadow.camera.bottom = -30;
	directionalLight.shadow.camera.near = 0.1;
	directionalLight.shadow.camera.far = 100;
	directionalLight.shadow.mapSize.width = 4096; // Higher resolution shadows
	directionalLight.shadow.mapSize.height = 4096;
	directionalLight.shadow.bias = -0.0005; // Reduce shadow acne
	scene.add(directionalLight);

	// Add a hemisphere light for more natural lighting
	const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.4);
	hemiLight.position.set(0, 20, 0);
	scene.add(hemiLight);
}

// Load GLB model
function loadGLBModel() {
	const loader = new THREE.GLTFLoader();

	// Updated filename
	const modelPath = "/static/models/map3_GDG.glb";

	loader.load(
		modelPath,
		function (gltf) {
			const model = gltf.scene;

			// Get bounding box to understand model dimensions
			const box = new THREE.Box3().setFromObject(model);
			const center = box.getCenter(new THREE.Vector3());
			const size = box.getSize(new THREE.Vector3());

			console.log("Model bounds:", {
				min: box.min,
				max: box.max,
				center: center,
				size: size,
			});

			// Position model so its bottom sits at y=0
			model.position.x = -center.x;
			model.position.z = -center.z;
			model.position.y = -box.min.y; // This lifts the model so its bottom is at y=0

			// Scale the model if needed
			const maxDim = Math.max(size.x, size.y, size.z);
			const scale = 20 / maxDim; // Adjust this value based on your model
			model.scale.setScalar(scale);

			// Update camera position based on model size
			camera.position.set(
				size.x * scale * 0.5,
				size.y * scale * 0.5,
				size.z * scale * 0.5
			);
			camera.lookAt(0, 0, 0);
			controls.update();

			// Enable shadows and improve material quality for all meshes
			model.traverse((child) => {
				if (child.isMesh) {
					child.castShadow = true;
					child.receiveShadow = true;

					// Improve material quality
					if (child.material) {
						// Ensure proper encoding
						if (child.material.map)
							child.material.map.encoding = THREE.sRGBEncoding;

						// Add anisotropic filtering for textures
						if (child.material.map) {
							child.material.map.anisotropy =
								renderer.capabilities.getMaxAnisotropy();
							child.material.map.minFilter = THREE.LinearMipmapLinearFilter;
							child.material.map.magFilter = THREE.LinearFilter;
						}

						// Ensure materials update
						child.material.needsUpdate = true;
					}

					// Store building information
					// Check if mesh name matches any building code
					const meshName = child.name || "";

					// First try exact match
					let matchingCode = BUILDING_CODES.find(
						(code) =>
							meshName === code || meshName.toUpperCase() === code.toUpperCase()
					);

					// If no exact match, try more specific patterns
					if (!matchingCode) {
						// Sort codes by length (longest first) to match more specific codes first
						const sortedCodes = [...BUILDING_CODES].sort(
							(a, b) => b.length - a.length
						);

						matchingCode = sortedCodes.find((code) => {
							// Check if mesh name contains the code as a separate word/segment
							const regex = new RegExp(`\\b${code}\\b`, "i");
							return (
								regex.test(meshName) ||
								meshName.includes(code + "_") ||
								meshName.includes(code + "-") ||
								meshName.includes(code + " ") ||
								meshName.endsWith(code)
							);
						});
					}

					if (matchingCode) {
						// Clone material to avoid affecting other objects
						child.material = child.material.clone();

						buildings.push({
							mesh: child,
							code: matchingCode,
							originalColor: child.material.color
								? child.material.color.getHex()
								: 0xffffff,
							originalEmissive: child.material.emissive
								? child.material.emissive.getHex()
								: 0x000000,
						});

						// Make building interactive
						child.userData.isBuilding = true;
						child.userData.buildingCode = matchingCode;

						console.log(
							"Found building:",
							matchingCode,
							"Mesh name:",
							meshName
						);
					}
				}
			});

			scene.add(model);

			// Log found buildings
			console.log(
				`Found ${buildings.length} buildings in the model:`,
				buildings.map((b) => b.code).join(", ")
			);

			// Populate legend
			populateLegend();

			// Hide loading indicator
			if (loadingIndicator) {
				loadingIndicator.style.display = "none";
			}

			// Start animation loop
			animate();
		},
		function (xhr) {
			// Progress callback
			const percentComplete = (xhr.loaded / xhr.total) * 100;
			console.log("Loading: " + percentComplete.toFixed(2) + "%");
		},
		function (error) {
			console.error("Error loading GLB model:", error);
			if (loadingIndicator) {
				loadingIndicator.innerHTML =
					'<p class="text-danger">Error loading 3D map. Please refresh the page.</p>';
			}

			// Add placeholder buildings for testing
			addPlaceholderBuildings();
			animate();
		}
	);
}

// Add placeholder buildings if GLB fails to load
function addPlaceholderBuildings() {
	const buildingData = [
		{ code: "SCA", position: [-5, 0, -5], color: 0x4169e1 },
		{ code: "SCB", position: [5, 0, -5], color: 0x32cd32 },
		{ code: "FC", position: [0, 0, 5], color: 0xff6347 },
	];

	buildingData.forEach((data) => {
		const geometry = new THREE.BoxGeometry(4, 6, 4);
		const material = new THREE.MeshStandardMaterial({
			color: data.color,
			roughness: 0.7,
			metalness: 0.3,
		});
		const building = new THREE.Mesh(geometry, material);
		building.position.set(...data.position);
		building.position.y = 3; // Half height above ground
		building.castShadow = true;
		building.receiveShadow = true;
		building.userData.isBuilding = true;
		building.userData.buildingCode = data.code;

		scene.add(building);

		buildings.push({
			mesh: building,
			code: data.code,
			originalColor: data.color,
		});
	});

	if (loadingIndicator) {
		loadingIndicator.style.display = "none";
	}
}

// Handle mouse click
function onMouseClick(event) {
	// Check if modal is open
	const modal = bootstrap.Modal.getInstance(
		document.getElementById("buildingModal")
	);
	if (modal && modal._isShown) {
		return; // Disable clicks when modal is open
	}

	const rect = renderer.domElement.getBoundingClientRect();
	mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
	mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

	raycaster.setFromCamera(mouse, camera);

	// Check for intersections with buildings
	const intersects = raycaster.intersectObjects(scene.children, true);

	for (let i = 0; i < intersects.length; i++) {
		const object = intersects[i].object;
		if (object.userData.isBuilding) {
			// Highlight the building
			highlightBuilding(object);

			// Show building modal
			showBuildingModal(object.userData.buildingCode);
			break;
		}
	}
}

// Highlight building with color change only
function highlightBuilding(buildingMesh) {
	// Reset previous selection
	if (selectedBuilding) {
		const buildingInfo = buildings.find((b) => b.mesh === selectedBuilding);
		if (buildingInfo) {
			// Reset to original color
			selectedBuilding.material.color.setHex(buildingInfo.originalColor);
			if (selectedBuilding.material.emissive) {
				selectedBuilding.material.emissive.setHex(
					buildingInfo.originalEmissive
				);
			}
		}
	}

	// Highlight new selection
	selectedBuilding = buildingMesh;
	const buildingInfo = buildings.find((b) => b.mesh === buildingMesh);

	if (buildingInfo) {
		// Change color to red
		buildingMesh.material.color.setHex(0xff0000); // Red color
		if (buildingMesh.material.emissive) {
			buildingMesh.material.emissive.setHex(0x440000); // Slight red glow
			buildingMesh.material.emissiveIntensity = 0.3;
		}

		// Update legend selection
		updateLegendSelection(buildingInfo.code);
	}
}

// Handle window resize
function onWindowResize() {
	const container = document.getElementById("map-container");
	camera.aspect = container.clientWidth / container.clientHeight;
	camera.updateProjectionMatrix();
	renderer.setSize(container.clientWidth, container.clientHeight);
}

// Animation loop
function animate() {
	requestAnimationFrame(animate);

	// Update controls
	controls.update();

	// Render scene
	renderer.render(scene, camera);
}

// Show building modal
function showBuildingModal(buildingCode) {
	const modalElement = document.getElementById("buildingModal");
	if (!modalElement) {
		console.error("Modal element not found");
		return;
	}

	let modal = bootstrap.Modal.getInstance(modalElement);
	if (!modal) {
		modal = new bootstrap.Modal(modalElement, {
			keyboard: true,
			backdrop: true,
		});
	}

	// Update modal content
	const nameEl = document.getElementById("building-name");
	const descEl = document.getElementById("building-description");
	const titleEl = document.getElementById("buildingModalLabel");

	if (nameEl) nameEl.textContent = BUILDING_NAMES[buildingCode] || buildingCode;
	if (descEl)
		descEl.textContent =
			BUILDING_DESCRIPTIONS[buildingCode] || "No description available.";
	if (titleEl)
		titleEl.textContent = BUILDING_NAMES[buildingCode] || "Building Details";

	// For now, show appropriate message based on building
	const sportsFacilities = [
		"GDG-SPRT",
		"GDG-STD",
		"GDG-BAS1",
		"GDG-BAS2",
		"GDG-GSG",
	];

	const sportsSection = document.getElementById("sports-rooms-section");
	const noSportsSection = document.getElementById("no-sports-rooms");
	const sportsList = document.getElementById("sports-rooms-list");

	if (sportsFacilities.includes(buildingCode)) {
		if (sportsSection) sportsSection.style.display = "block";
		if (noSportsSection) noSportsSection.style.display = "none";
		if (sportsList)
			sportsList.innerHTML =
				'<p class="text-muted">Loading sports rooms...</p>';

		// Show book button for logged in users
		const bookBtn = document.getElementById("book-room-btn");
		if (bookBtn) bookBtn.style.display = "block";
	} else {
		if (sportsSection) sportsSection.style.display = "none";
		if (noSportsSection) noSportsSection.style.display = "block";

		// Hide book button
		const bookBtn = document.getElementById("book-room-btn");
		if (bookBtn) bookBtn.style.display = "none";
	}

	const buildingCodeInput = document.getElementById("booking-building-code");
	if (buildingCodeInput) {
		buildingCodeInput.value = buildingCode;
	}

	fetch(`/api/sports_rooms/${buildingCode}`)
		.then((res) => res.json())
		.then((rooms) => {
			const roomSelect = document.getElementById("sports-room");
			roomSelect.innerHTML = "";

			if (rooms.length === 0) {
				const option = document.createElement("option");
				option.textContent = "No rooms available";
				option.disabled = true;
				roomSelect.appendChild(option);
			} else {
				rooms.forEach((room) => {
					const option = document.createElement("option");
					option.value = room.id;
					option.textContent = `${room.name} (Capacity: ${room.capacity})`;
					roomSelect.appendChild(option);
				});
			}
		});

	modal.show();
}

// Populate legend with building list
function populateLegend() {
	const academicContainer = document.getElementById("academic-buildings");
	if (!academicContainer) return;

	// Get all buildings except sports facilities
	const nonSportsBuildings = buildings.filter(
		(b) => b.code !== "GDG-SPRT" && b.code !== "GDG-STD"
	);

	// Sort alphabetically by code
	nonSportsBuildings.sort((a, b) => a.code.localeCompare(b.code));

	// Create legend items
	nonSportsBuildings.forEach((building) => {
		const item = document.createElement("div");
		item.className = "legend-item";
		item.dataset.building = building.code;

		const nameSpan = document.createElement("span");
		nameSpan.className = "building-name";
		nameSpan.textContent = BUILDING_NAMES[building.code] || building.code;

		const zoomBtn = document.createElement("button");
		zoomBtn.className = "btn btn-sm btn-outline-primary zoom-btn";
		zoomBtn.title = "Zoom to building";
		zoomBtn.innerHTML = '<i class="bi bi-arrow-right-circle"></i>';

		item.appendChild(nameSpan);
		item.appendChild(zoomBtn);
		academicContainer.appendChild(item);
	});

	// Add click handlers to all legend items
	setupLegendHandlers();
}

// Setup legend interaction handlers
function setupLegendHandlers() {
	// Toggle sidebar
	const sidebar = document.getElementById("legend-sidebar");
	const toggleBtn = document.getElementById("toggle-sidebar");
	const showBtn = document.getElementById("show-sidebar");

	toggleBtn?.addEventListener("click", () => {
		sidebar.style.display = "none";
		showBtn.style.display = "block";
	});

	showBtn?.addEventListener("click", () => {
		sidebar.style.display = "block";
		showBtn.style.display = "none";
	});

	// Legend item clicks
	document.querySelectorAll(".legend-item").forEach((item) => {
		// Click on item name to highlight
		item.addEventListener("click", (e) => {
			if (!e.target.closest(".zoom-btn")) {
				const buildingCode = item.dataset.building;
				const building = buildings.find((b) => b.code === buildingCode);
				if (building) {
					highlightBuilding(building.mesh);
					updateLegendSelection(buildingCode);
					showBuildingModal(buildingCode);
				}
			}
		});

		// Click on zoom button
		const zoomBtn = item.querySelector(".zoom-btn");
		zoomBtn?.addEventListener("click", (e) => {
			e.stopPropagation();
			const buildingCode = item.dataset.building;
			zoomToBuilding(buildingCode);
		});
	});
}

// Update legend selection visual
function updateLegendSelection(buildingCode) {
	document.querySelectorAll(".legend-item").forEach((item) => {
		if (item.dataset.building === buildingCode) {
			item.classList.add("active");
		} else {
			item.classList.remove("active");
		}
	});
}

// Zoom camera to specific building
function zoomToBuilding(buildingCode) {
	const building = buildings.find((b) => b.code === buildingCode);
	if (!building) return;

	// Get building bounds
	const box = new THREE.Box3().setFromObject(building.mesh);
	const center = box.getCenter(new THREE.Vector3());
	const size = box.getSize(new THREE.Vector3());

	// Calculate optimal camera position
	const maxDim = Math.max(size.x, size.y, size.z);
	const fov = camera.fov * (Math.PI / 180);
	const distance = Math.abs(maxDim / Math.sin(fov / 2));

	// Animate camera to new position
	const targetPosition = new THREE.Vector3(
		center.x + distance * 0.7,
		center.y + distance * 0.5,
		center.z + distance * 0.7
	);

	animateCameraToPosition(targetPosition, center, () => {
		// Highlight building after zoom
		highlightBuilding(building.mesh);
		updateLegendSelection(buildingCode);
	});
}

// Animate camera movement
function animateCameraToPosition(targetPosition, targetLookAt, onComplete) {
	const startPosition = camera.position.clone();
	const startLookAt = controls.target.clone();
	const duration = 1000; // 1 second
	const startTime = Date.now();

	function updateCamera() {
		const elapsed = Date.now() - startTime;
		const progress = Math.min(elapsed / duration, 1);

		// Easing function
		const easeProgress = 1 - Math.pow(1 - progress, 3);

		// Interpolate position
		camera.position.lerpVectors(startPosition, targetPosition, easeProgress);

		// Interpolate look at
		controls.target.lerpVectors(startLookAt, targetLookAt, easeProgress);

		controls.update();

		if (progress < 1) {
			requestAnimationFrame(updateCamera);
		} else if (onComplete) {
			onComplete();
		}
	}

	updateCamera();
}

// Initialize when page loads
document.addEventListener("DOMContentLoaded", function () {
	// Verify modal exists before initializing 3D map
	const modalCheck = document.getElementById("buildingModal");
	if (!modalCheck) {
		console.warn("Building modal not found, waiting for DOM...");
		setTimeout(() => {
			init();
		}, 500);
	} else {
		init();
	}
});
