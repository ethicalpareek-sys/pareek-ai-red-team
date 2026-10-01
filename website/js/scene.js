// scene.js
const canvas = document.getElementById('canvas');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0e27);
scene.fog = new THREE.Fog(0x0a0e27, 20, 90);

const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 0, 28);

const group = new THREE.Group();
scene.add(group);

const ambient = new THREE.AmbientLight(0xffffff, 0.7);
scene.add(ambient);

const pointLight = new THREE.PointLight(0x00ff88, 1.5, 100);
pointLight.position.set(10, 10, 15);
scene.add(pointLight);

const pointLight2 = new THREE.PointLight(0x00ccff, 1.2, 100);
pointLight2.position.set(-12, -8, 14);
scene.add(pointLight2);

const ringMaterial = new THREE.MeshStandardMaterial({
    color: 0x00ff88,
    emissive: 0x00ff88,
    emissiveIntensity: 0.5,
    metalness: 0.8,
    roughness: 0.3,
    transparent: true,
    opacity: 0.9,
});

const ringGeometry = new THREE.TorusGeometry(7, 0.08, 16, 100);
const ring = new THREE.Mesh(ringGeometry, ringMaterial);
ring.rotation.x = Math.PI / 2.2;
ring.rotation.y = Math.PI / 4;
group.add(ring);

const ring2 = new THREE.Mesh(ringGeometry, new THREE.MeshStandardMaterial({
    color: 0x00ccff,
    emissive: 0x00ccff,
    emissiveIntensity: 0.5,
    metalness: 0.6,
    roughness: 0.3,
    transparent: true,
    opacity: 0.8,
}));
ring2.rotation.x = Math.PI / 3;
ring2.rotation.y = Math.PI / 5;
ring2.scale.set(1.2, 1.2, 1.2);
group.add(ring2);

const sphereMaterial = new THREE.MeshStandardMaterial({
    color: 0x0c1b3a,
    emissive: 0x0033cc,
    emissiveIntensity: 0.6,
    metalness: 0.9,
    roughness: 0.2,
    transparent: true,
    opacity: 0.88,
});

const sphere = new THREE.Mesh(new THREE.IcosahedronGeometry(3, 1), sphereMaterial);
group.add(sphere);

const particleGeometry = new THREE.BufferGeometry();
const particleCount = 600;
const positions = [];

for (let i = 0; i < particleCount; i++) {
    const theta = Math.random() * Math.PI * 2;
    const radius = 8 + Math.random() * 20;
    const y = (Math.random() - 0.5) * 18;
    positions.push(
        Math.cos(theta) * radius,
        y,
        Math.sin(theta) * radius
    );
}

particleGeometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));

const particles = new THREE.Points(
    particleGeometry,
    new THREE.PointsMaterial({
        color: 0x00ff88,
        size: 0.08,
        transparent: true,
        opacity: 0.8,
    })
);
scene.add(particles);

const lineMaterial = new THREE.LineBasicMaterial({ color: 0x00ccff, transparent: true, opacity: 0.6 });

for (let i = 0; i < 20; i++) {
    const points = [];
    const start = new THREE.Vector3(
        (Math.random() - 0.5) * 25,
        (Math.random() - 0.5) * 20,
        (Math.random() - 0.5) * 25
    );
    points.push(start);

    for (let j = 1; j <= 5; j++) {
        points.push(new THREE.Vector3(
            start.x + (Math.random() - 0.5) * 6,
            start.y + (Math.random() - 0.5) * 6,
            start.z + (Math.random() - 0.5) * 6
        ));
    }

    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const line = new THREE.Line(geometry, lineMaterial);
    scene.add(line);
}

let mouseX = 0;
let mouseY = 0;

window.addEventListener('mousemove', (event) => {
    mouseX = (event.clientX / window.innerWidth) * 2 - 1;
    mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
});

function animate() {
    requestAnimationFrame(animate);

    const time = performance.now() * 0.001;

    group.rotation.y += 0.003;
    group.rotation.x = mouseY * 0.4;
    group.rotation.z = mouseX * 0.2;

    ring.rotation.z += 0.004;
    ring2.rotation.z -= 0.006;
    sphere.rotation.y += 0.006;
    sphere.rotation.x += 0.003;
    particles.rotation.y += 0.0015;

    renderer.render(scene, camera);
}

animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
