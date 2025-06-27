let scene, camera, renderer, controls;
let raycaster, mouse;
let buildings = [];
let selectedBuilding = null;
let buildingMeta = {}; // Holds building metadata by code
let loadingIndicator;

async function init() {
	loadingIndicator = document.getElementById("loading-indicator");
	const container = document.getElementById("map-container");

	scene = new THREE.Scene();
	scene.background = new THREE.Color(0xf5f5f5);

	camera = new THREE.PerspectiveCamera(
		75,
		container.clientWidth / container.clientHeight,
		0.01,
		1000
	);
	camera.position.set(10, 10, 10);
	camera.lookAt(0, 0, 0);

	renderer = new THREE.WebGLRenderer({
		antialias: true,
		alpha: true,
		powerPreference: "high-performance",
	});
	renderer.setSize(container.clientWidth, container.clientHeight);
	renderer.shadowMap.enabled = true;
	renderer.shadowMap.type = THREE.VSMShadowMap;
	renderer.setPixelRatio(window.devicePixelRatio);
	renderer.toneMapping = THREE.ACESFilmicToneMapping;
	renderer.toneMappingExposure = 1;
	renderer.outputEncoding = THREE.sRGBEncoding;
	container.appendChild(renderer.domElement);

	controls = new THREE.OrbitControls(camera, renderer.domElement);
	controls.enableDamping = true;
	controls.dampingFactor = 0.05;
	controls.minDistance = 0.5;
	controls.maxDistance = 50;
	controls.maxPolarAngle = Math.PI / 2;
	controls.screenSpacePanning = false;

	setupLighting();

	raycaster = new THREE.Raycaster();
	mouse = new THREE.Vector2();

	try {
		await fetchBuildingMeta();
		await loadGLBModel();
		populateLegend();
	} catch (err) {
		console.error("Initialization failed:", err);
		addPlaceholderBuildings();
	}

	window.addEventListener("resize", onWindowResize);
	container.addEventListener("click", onMouseClick);
	container.addEventListener("mousemove", onMouseMove);

	animate();
}

async function fetchBuildingMeta() {
	const res = await fetch("/api/buildings_with_sports_flag");
	const data = await res.json();

	if (!Array.isArray(data)) throw new Error("Invalid building metadata");

	data.forEach((b) => {
		buildingMeta[b.code] = {
			name: b.name,
			description: b.description,
			image_url:
				b.image_url || "https://via.placeholder.com/300x200?text=No+Image",
			has_sports_room: Boolean(b.has_sports_room),
		};
	});
}

function setupLighting() {
	const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
	scene.add(ambientLight);

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

	const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.4);
	hemiLight.position.set(0, 20, 0);
	scene.add(hemiLight);
}

async function loadGLBModel() {
	const loader = new THREE.GLTFLoader();
	const modelPath = "/static/models/map3_GDG.glb";

	return new Promise((resolve, reject) => {
		loader.load(
			modelPath,
			(gltf) => {
				const model = gltf.scene;
				const box = new THREE.Box3().setFromObject(model);
				const center = box.getCenter(new THREE.Vector3());
				const size = box.getSize(new THREE.Vector3());

				model.position.set(-center.x, -box.min.y, -center.z);
				const scale = 20 / Math.max(size.x, size.y, size.z);
				model.scale.setScalar(scale);

				camera.position.set(
					size.x * scale * 0.5,
					size.y * scale * 0.5,
					size.z * scale * 0.5
				);
				camera.lookAt(0, 0, 0);
				controls.update();

				model.traverse((child) => {
					if (child.isMesh) {
						const meshName = child.name || "";

						// 🔧 FIX: Use exact match or word boundaries to avoid partial matches
						const matchCode = Object.keys(buildingMeta).find((code) => {
							// Try exact match first
							if (meshName === code) return true;

							// If not exact, check if code exists as a complete word/segment
							// This prevents "GDG-F" from matching "GDG-FIF"
							const regex = new RegExp(`\\b${code.replace(/[-]/g, "\\-")}\\b`);
							return regex.test(meshName);
						});

						if (matchCode) {
							child.material = child.material.clone();
							child.castShadow = true;
							child.receiveShadow = true;
							child.userData.isBuilding = true;
							child.userData.buildingCode = matchCode;

							// 🎨 Set building colors based on type
							const meta = buildingMeta[matchCode];
							let idleColor, activeColor;

							if (meta && meta.has_sports_room) {
								// Sports facilities: Red theme
								idleColor = 0xff8282; // Light red
								activeColor = 0xdc2525; // Dark red
							} else {
								// Academic buildings: Blue theme
								idleColor = 0x91c8e4; // Light blue
								activeColor = 0x102e50; // Dark blue
							}

							// Apply idle color initially
							child.material.color.setHex(idleColor);

							buildings.push({
								mesh: child,
								code: matchCode,
								originalColor: idleColor,
								activeColor: activeColor,
								originalEmissive: child.material.emissive?.getHex() || 0x000000,
								isSports: meta && meta.has_sports_room,
							});
						}
					}
				});

				scene.add(model);
				if (loadingIndicator) loadingIndicator.style.display = "none";
				resolve();
			},
			undefined,
			(err) => {
				console.error("GLB loading failed:", err);
				if (loadingIndicator)
					loadingIndicator.innerHTML = "<p>Error loading 3D map.</p>";
				reject(err);
			}
		);
	});
}

function animate() {
	requestAnimationFrame(animate);
	controls.update();
	renderer.render(scene, camera);
}

function onWindowResize() {
	const container = document.getElementById("map-container");
	camera.aspect = container.clientWidth / container.clientHeight;
	camera.updateProjectionMatrix();
	renderer.setSize(container.clientWidth, container.clientHeight);
}

function onMouseMove(event) {
	const rect = renderer.domElement.getBoundingClientRect();
	mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
	mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
	raycaster.setFromCamera(mouse, camera);

	const intersects = raycaster.intersectObjects(scene.children, true);
	renderer.domElement.style.cursor = "default";
	for (const hit of intersects) {
		if (hit.object.userData.isBuilding) {
			renderer.domElement.style.cursor = "pointer";
			break;
		}
	}
}

function onMouseClick(event) {
	const rect = renderer.domElement.getBoundingClientRect();
	mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
	mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
	raycaster.setFromCamera(mouse, camera);

	const intersects = raycaster.intersectObjects(scene.children, true);
	for (const hit of intersects) {
		if (hit.object.userData.isBuilding) {
			highlightBuilding(hit.object);
			showBuildingModal(hit.object.userData.buildingCode);
			break;
		}
	}
}

function highlightBuilding(mesh) {
	// Reset previously selected building to its original color
	if (selectedBuilding) {
		const prev = buildings.find((b) => b.mesh === selectedBuilding);
		if (prev) {
			selectedBuilding.material.color.setHex(prev.originalColor);
			if (selectedBuilding.material.emissive)
				selectedBuilding.material.emissive.setHex(prev.originalEmissive);
		}
	}

	selectedBuilding = mesh;
	const b = buildings.find((b) => b.mesh === mesh);
	if (b) {
		// Set to active color (darker version)
		mesh.material.color.setHex(b.activeColor);
		if (mesh.material.emissive) {
			mesh.material.emissive.setHex(0x000000);
			mesh.material.emissiveIntensity = 0.1;
		}
		updateLegendSelection(b.code);
	}
}

// Fetch and show approved & upcoming bookings
function loadActiveBookings(buildingCode) {
	const sectionEl = document.getElementById("active-bookings-section");
	const tableBody = document.getElementById("active-bookings-body");

	const hariIndonesia = [
		"Minggu",
		"Senin",
		"Selasa",
		"Rabu",
		"Kamis",
		"Jumat",
		"Sabtu",
	];

	function formatTanggalIndo(dateStr) {
		const date = new Date(dateStr);
		const hari = hariIndonesia[date.getDay()];
		const tgl = date.toLocaleDateString("id-ID", {
			day: "2-digit",
			month: "short",
			year: "numeric",
		});
		return `${hari}, ${tgl}`;
	}

	function formatJam(jamStr) {
		// contoh input: "6:00:00" → "06.00 WIB"
		const [jam, menit] = jamStr.split(":");
		return `${jam.padStart(2, "0")}.${menit} WIB`;
	}

	sectionEl.style.display = "block";
	tableBody.innerHTML = `
    <tr><td colspan="5" class="text-muted">Memuat jadwal...</td></tr>
  `;

	fetch(`/api/bookings/active/${buildingCode}`)
		.then((res) => res.json())
		.then((data) => {
			tableBody.innerHTML = "";

			if (!data || data.length === 0) {
				tableBody.innerHTML = `
          <tr><td colspan="5" class="text-muted">Tidak ada jadwal aktif.</td></tr>
        `;
				return;
			}

			data.forEach((booking, index) => {
				const row = document.createElement("tr");
				row.innerHTML = `
          <td>${index + 1}</td>
          <td>${booking.username}</td>
  				<td>${formatTanggalIndo(booking.booking_date)}</td>
					<td>${formatJam(booking.start_time)}</td>
					<td>${formatJam(booking.end_time)}</td>
        `;
				tableBody.appendChild(row);
			});
		})
		.catch(() => {
			tableBody.innerHTML = `
        <tr><td colspan="5" class="text-danger">Gagal memuat jadwal.</td></tr>
      `;
		});
}

let calendarInstance = null;

function initCalendar(roomId) {
	const input = document.getElementById("booking-date");
	if (!input || !roomId) {
		console.warn("booking-date input atau roomId tidak ditemukan.");
		return;
	}

	// Hancurkan instance sebelumnya jika ada
	if (calendarInstance) {
		calendarInstance.destroy();
		calendarInstance = null;
	}

	fetch(`/api/room_booked_dates/${roomId}`)
		.then((res) => res.json())
		.then((dates) => {
			calendarInstance = flatpickr(input, {
				dateFormat: "Y-m-d",
				minDate: "today",
				disableMobile: true,
				onDayCreate: function (dObj, dStr, fp, dayElem) {
					const date = dayElem.dateObj.toISOString().split("T")[0];
					if (dates.includes(date)) {
						dayElem.classList.add("bg-warning", "text-dark");
						dayElem.title = "Sudah ada peminjaman";
					}
				},
				onChange: function (selectedDates, dateStr) {
					if (roomId && dateStr) {
						input.value = dateStr;
						disableConflictTimes(roomId, dateStr);
					}
				},
			});
		});
}

function disableConflictTimes(roomId, dateStr) {
	const startSelect = document.getElementById("start-time");
	const endSelect = document.getElementById("end-time");
	if (!roomId || !dateStr || !startSelect || !endSelect) return;

	fetch(`/api/room_schedule/${roomId}?date=${dateStr}`)
		.then((res) => res.json())
		.then((data) => {
			const usedSlots = new Set();

			data.forEach((booking) => {
				const start = parseInt(booking.start_time.split(":")[0]);
				const end = parseInt(booking.end_time.split(":")[0]);
				for (let i = start; i < end; i++) {
					usedSlots.add(i);
				}
			});

			// Reset semua opsi
			[...startSelect.options].forEach((opt) => {
				opt.disabled = false;
				opt.textContent = opt.value;
				opt.classList.remove("text-danger");
			});

			[...endSelect.options].forEach((opt) => {
				opt.disabled = false;
				opt.textContent = opt.value;
				opt.classList.remove("text-danger");
			});

			// Tandai jam bentrok
			[...startSelect.options].forEach((opt) => {
				const hour = parseInt(opt.value.split(":")[0]);
				if (usedSlots.has(hour)) {
					opt.disabled = true;
					opt.textContent += " (terpakai)";
					opt.classList.add("text-danger");
				}
			});

			[...endSelect.options].forEach((opt) => {
				const hour = parseInt(opt.value.split(":")[0]);
				if (usedSlots.has(hour - 1)) {
					opt.disabled = true;
					opt.textContent += " (terpakai)";
					opt.classList.add("text-danger");
				}
			});
		});
}

function showBuildingModal(buildingCode) {
	const modalElement = document.getElementById("buildingModal");
	if (!modalElement) return;

	const meta = buildingMeta[buildingCode];
	if (!meta) return;

	// Isi data gedung
	document.getElementById("building-name").textContent =
		meta.name || buildingCode;
	document.getElementById("building-description").textContent =
		meta.description || "Tidak ada deskripsi.";
	document.getElementById("building-image").src =
		meta.image_url || "https://via.placeholder.com/300x200";

	const sportsSection = document.getElementById("sports-rooms-section");
	const noSportsSection = document.getElementById("no-sports-rooms");
	const bookingCodeInput = document.getElementById("booking-building-code");
	const roomSelect = document.getElementById("sports-room");
	const roomImage = document.getElementById("sports-room-image");

	const activeSection = document.getElementById("active-bookings-section");
	const activeList = document.getElementById("active-bookings-list");

	const isSports = meta.has_sports_room;

	if (isSports) {
		// Tampilkan form & jadwal
		sportsSection?.style?.setProperty("display", "block");
		noSportsSection?.style?.setProperty("display", "none");
		activeSection?.style?.setProperty("display", "block");

		if (bookingCodeInput) bookingCodeInput.value = buildingCode;

		// Load daftar ruangan olahraga
		roomSelect.innerHTML = "<option>Memuat data ruangan...</option>";
		roomImage.src = "https://via.placeholder.com/300x200?text=Memuat+Gambar";

		fetch(`/api/sports_rooms/${buildingCode}`)
			.then((res) => res.json())
			.then((rooms) => {
				roomSelect.innerHTML = "";
				if (!rooms.length) {
					const opt = document.createElement("option");
					opt.textContent = "Tidak ada ruangan tersedia";
					opt.disabled = true;
					roomSelect.appendChild(opt);
					roomImage.src =
						"https://via.placeholder.com/300x200?text=Tidak+Ada+Ruangan";
					return;
				}

				// Tambahkan options
				rooms.forEach((room, index) => {
					const opt = document.createElement("option");
					opt.value = room.id;
					opt.textContent = `${room.name} (Kapasitas: ${room.capacity})`;
					opt.dataset.image = room.image_url || "";
					roomSelect.appendChild(opt);

					// Gambar default dari ruangan pertama
					if (index === 0 && room.image_url) {
						roomImage.src = room.image_url;
					}
				});

				// Ganti gambar saat dropdown berubah
				roomSelect.addEventListener("change", function () {
					const selectedOption = this.options[this.selectedIndex];
					const imgUrl =
						selectedOption.dataset.image ||
						"https://via.placeholder.com/300x200?text=Gambar+Tidak+Tersedia";
					roomImage.src = imgUrl;
				});

				// Trigger perubahan awal jika tersedia
				if (roomSelect.options.length > 0) {
					roomSelect.dispatchEvent(new Event("change"));
				}

				// ✅ Tambahkan ini
				const selectedRoomId = roomSelect.value;
				if (selectedRoomId) {
					initCalendar(selectedRoomId);
				}
			});

		// Load jadwal aktif
		if (activeList) {
			activeList.innerHTML =
				'<li class="list-group-item text-muted">Memuat jadwal...</li>';

			fetch(`/api/bookings/active/${buildingCode}`)
				.then((res) => res.json())
				.then((data) => {
					activeList.innerHTML = "";
					if (!data || data.length === 0) {
						activeList.innerHTML =
							'<li class="list-group-item text-muted">Tidak ada jadwal aktif.</li>';
						return;
					}
					data.forEach((b) => {
						const item = document.createElement("li");
						item.className = "list-group-item";
						item.innerHTML = `<strong>${b.room_name}</strong> — ${b.start_time} s/d ${b.end_time}`;
						activeList.appendChild(item);
					});
				})
				.catch(() => {
					activeList.innerHTML =
						'<li class="list-group-item text-danger">Gagal memuat jadwal.</li>';
				});
		}
	} else {
		// Bukan gedung olahraga → sembunyikan form & jadwal
		sportsSection?.style?.setProperty("display", "none");
		noSportsSection?.style?.setProperty("display", "block");
		activeSection?.style?.setProperty("display", "none");
		if (activeList) activeList.innerHTML = "";
	}

	loadActiveBookings(buildingCode);

	// Tampilkan modal
	new bootstrap.Modal(modalElement).show();
}

function populateLegend() {
	const academicContainer = document.getElementById("academic-buildings");
	const sportsContainer = document.getElementById("sports-buildings");

	if (!academicContainer || !sportsContainer) return;

	Object.entries(buildingMeta).forEach(([code, meta]) => {
		const item = document.createElement("div");
		item.className = "legend-item";
		item.dataset.building = code;

		const nameSpan = document.createElement("span");
		nameSpan.className = "building-name";
		nameSpan.textContent = meta.name || code;

		const zoomBtn = document.createElement("button");
		zoomBtn.className = "btn btn-sm btn-outline-primary zoom-btn";
		zoomBtn.innerHTML = '<i class="bi bi-arrow-right-circle"></i>';

		item.appendChild(nameSpan);
		item.appendChild(zoomBtn);

		if (meta.has_sports_room) {
			sportsContainer.appendChild(item);
		} else {
			academicContainer.appendChild(item);
		}
	});

	setupLegendHandlers();
}

function setupLegendHandlers() {
	document.querySelectorAll(".legend-item").forEach((item) => {
		item.addEventListener("click", (e) => {
			if (!e.target.closest(".zoom-btn")) {
				const code = item.dataset.building;
				const building = buildings.find((b) => b.code === code);
				if (building) {
					highlightBuilding(building.mesh);
					showBuildingModal(code);
				}
			}
		});
		item.querySelector(".zoom-btn")?.addEventListener("click", (e) => {
			e.stopPropagation();
			const code = item.dataset.building;
			zoomToBuilding(code);
		});
	});

	document.getElementById("toggle-sidebar")?.addEventListener("click", () => {
		document.getElementById("legend-sidebar").style.display = "none";
		document.getElementById("show-sidebar").style.display = "block";
	});

	document.getElementById("show-sidebar")?.addEventListener("click", () => {
		document.getElementById("legend-sidebar").style.display = "block";
		document.getElementById("show-sidebar").style.display = "none";
	});
}

function updateLegendSelection(code) {
	document.querySelectorAll(".legend-item").forEach((item) => {
		item.classList.toggle("active", item.dataset.building === code);
	});
}

function zoomToBuilding(code) {
	const b = buildings.find((b) => b.code === code);
	if (!b) return;

	// Highlight the building when zooming to it
	highlightBuilding(b.mesh);

	const box = new THREE.Box3().setFromObject(b.mesh);
	const center = box.getCenter(new THREE.Vector3());
	const size = box.getSize(new THREE.Vector3());
	const distance =
		Math.max(size.x, size.y, size.z) / Math.sin((camera.fov * Math.PI) / 360);

	const targetPos = new THREE.Vector3(
		center.x + distance * 0.7,
		center.y + distance * 0.5,
		center.z + distance * 0.7
	);
	animateCameraToPosition(targetPos, center);
}

function animateCameraToPosition(targetPos, lookAt, callback) {
	const start = camera.position.clone();
	const startLook = controls.target.clone();
	const duration = 1000;
	const startTime = Date.now();

	function step() {
		const t = (Date.now() - startTime) / duration;
		if (t < 1) {
			const ease = 1 - Math.pow(1 - t, 3);
			camera.position.lerpVectors(start, targetPos, ease);
			controls.target.lerpVectors(startLook, lookAt, ease);
			controls.update();
			requestAnimationFrame(step);
		} else {
			if (callback) callback();
		}
	}

	step();
}

function addPlaceholderBuildings() {
	const fallbackBuildings = [
		{ code: "FAKE1", position: [-5, 0, -5], color: 0xff0000 },
		{ code: "FAKE2", position: [5, 0, -5], color: 0x00ff00 },
	];

	fallbackBuildings.forEach((data) => {
		const mesh = new THREE.Mesh(
			new THREE.BoxGeometry(4, 6, 4),
			new THREE.MeshStandardMaterial({ color: data.color })
		);
		mesh.position.set(...data.position);
		mesh.position.y = 3;
		mesh.castShadow = true;
		mesh.receiveShadow = true;
		mesh.userData.isBuilding = true;
		mesh.userData.buildingCode = data.code;
		scene.add(mesh);
		buildings.push({ mesh, code: data.code, originalColor: data.color });
	});
}

document.addEventListener("DOMContentLoaded", init);
