import { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import landDots from '../../data/land-points.json';
import { severityColor } from '../../lib/viz';
const landPositions = new Float32Array(landDots);
function xyz(lat, lng, r = 1) {
  const p = (lat * Math.PI) / 180,
    t = (lng * Math.PI) / 180;
  return [r * Math.cos(p) * Math.sin(t), r * Math.sin(p), r * Math.cos(p) * Math.cos(t)];
}
const pointVertex = `attribute float magnitude; attribute vec3 pointColor; varying vec3 color; void main(){color=pointColor;vec4 mv=modelViewMatrix*vec4(position,1.0);gl_Position=projectionMatrix*mv;gl_PointSize=magnitude*min(1.7,2.8/-mv.z);}`;
const pointFragment = `varying vec3 color; void main(){float d=length(gl_PointCoord-vec2(.5));if(d>.5)discard;float a=pow(1.0-d*2.0,1.5);gl_FragColor=vec4(color,a*.94);}`;
export default function Globe({ locations, year = null, hero = false }) {
  const mount = useRef(),
    engine = useRef(),
    current = useRef({ locations, year }),
    [failed, setFailed] = useState(false);
  useEffect(() => {
    current.current = { locations, year };
    if (engine.current) engine.current.update();
  }, [locations, year]);
  useEffect(() => {
    const host = mount.current;
    let renderer;
    try {
      renderer = new THREE.WebGLRenderer({
        antialias: true,
        alpha: true,
        powerPreference: 'low-power',
      });
    } catch {
      setFailed(true);
      return;
    }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.8));
    renderer.setClearColor(0x000000, 0);
    host.appendChild(renderer.domElement);
    const scene = new THREE.Scene(),
      camera = new THREE.PerspectiveCamera(38, 1, 0.1, 20);
    camera.position.z = 3.65;
    const world = new THREE.Group();
    scene.add(world);
    world.rotation.y = -0.62;
    world.rotation.x = 0.15;
    const sphere = new THREE.Mesh(
      new THREE.SphereGeometry(0.996, 64, 48),
      new THREE.MeshPhongMaterial({ color: 0x111922, shininess: 3 }),
    );
    world.add(sphere);
    scene.add(new THREE.AmbientLight(0xb5c8e6, 1.2));
    const light = new THREE.DirectionalLight(0xbdd3ed, 1.5);
    light.position.set(-2, 3, 4);
    scene.add(light);
    const landGeo = new THREE.BufferGeometry();
    landGeo.setAttribute('position', new THREE.BufferAttribute(landPositions, 3));
    world.add(
      new THREE.Points(
        landGeo,
        new THREE.PointsMaterial({
          size: 0.008,
          color: 0x748190,
          transparent: true,
          opacity: 0.61,
          sizeAttenuation: true,
        }),
      ),
    );
    const gridPoints = [];
    for (let lat = -60; lat <= 60; lat += 30)
      for (let lng = -180; lng < 180; lng += 3)
        gridPoints.push(...xyz(lat, lng, 1.001), ...xyz(lat, lng + 3, 1.001));
    for (let lng = -180; lng < 180; lng += 30)
      for (let lat = -90; lat < 90; lat += 3)
        gridPoints.push(...xyz(lat, lng, 1.001), ...xyz(lat + 3, lng, 1.001));
    const gridGeo = new THREE.BufferGeometry();
    gridGeo.setAttribute('position', new THREE.Float32BufferAttribute(gridPoints, 3));
    world.add(
      new THREE.LineSegments(
        gridGeo,
        new THREE.LineBasicMaterial({ color: 0x566473, transparent: true, opacity: 0.16 }),
      ),
    );
    const halo = new THREE.Mesh(
      new THREE.SphereGeometry(1.03, 48, 32),
      new THREE.ShaderMaterial({
        uniforms: {},
        vertexShader: `varying vec3 n;varying vec3 v;void main(){n=normalize(normalMatrix*normal);vec4 mv=modelViewMatrix*vec4(position,1.0);v=normalize(-mv.xyz);gl_Position=projectionMatrix*mv;}`,
        fragmentShader: `varying vec3 n;varying vec3 v;void main(){float a=pow(1.0-max(dot(n,v),0.0),4.0)*.22;gl_FragColor=vec4(.45,.59,.74,a);}`,
        transparent: true,
        depthWrite: false,
        side: THREE.FrontSide,
      }),
    );
    world.add(halo);
    let eventPoints;
    function update() {
      if (eventPoints) {
        world.remove(eventPoints);
        eventPoints.geometry.dispose();
        eventPoints.material.dispose();
      }
      const { locations: loc, year: y } = current.current;
      if (!loc) return;
      let rows;
      if (y !== null) rows = loc[y] || [];
      else {
        const merged = new Map();
        Object.values(loc).forEach((a) =>
          a.forEach(([lat, lng, n, deaths]) => {
            const key = `${lat},${lng}`;
            if (merged.has(key)) {
              merged.get(key)[2] += n;
              merged.get(key)[3] += deaths;
            } else merged.set(key, [lat, lng, n, deaths]);
          }),
        );
        rows = [...merged.values()];
      }
      const pos = [],
        sizes = [],
        colors = [];
      rows.forEach(([lat, lng, n, deaths]) => {
        pos.push(...xyz(lat, lng, 1.009));
        sizes.push(Math.sqrt(n) * 1.1);
        const c = new THREE.Color(severityColor(deaths / n));
        colors.push(c.r, c.g, c.b);
      });
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
      g.setAttribute('magnitude', new THREE.Float32BufferAttribute(sizes, 1));
      g.setAttribute('pointColor', new THREE.Float32BufferAttribute(colors, 3));
      eventPoints = new THREE.Points(
        g,
        new THREE.ShaderMaterial({
          vertexShader: pointVertex,
          fragmentShader: pointFragment,
          transparent: true,
          depthWrite: false,
        }),
      );
      world.add(eventPoints);
      draw();
    }
    function draw() {
      renderer.render(scene, camera);
    }
    function resize() {
      const w = host.clientWidth,
        h = host.clientHeight;
      renderer.setSize(w, h);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      draw();
    }
    let dragging = false,
      lastX = 0,
      lastY = 0;
    const down = (e) => {
      if (e.isPrimary === false) return;
      dragging = true;
      lastX = e.clientX;
      lastY = e.clientY;
      host.setPointerCapture(e.pointerId);
    };
    const move = (e) => {
      if (!dragging) return;
      world.rotation.y += (e.clientX - lastX) * 0.007;
      world.rotation.x = THREE.MathUtils.clamp(
        world.rotation.x + (e.clientY - lastY) * 0.004,
        -0.7,
        0.7,
      );
      lastX = e.clientX;
      lastY = e.clientY;
      draw();
    };
    const up = () => {
      dragging = false;
    };
    const key = (e) => {
      if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home'].includes(e.key)) {
        e.preventDefault();
        if (e.key === 'Home') {
          world.rotation.set(0.15, -0.62, 0);
        } else {
          world.rotation.y += e.key === 'ArrowLeft' ? -0.15 : e.key === 'ArrowRight' ? 0.15 : 0;
          world.rotation.x = THREE.MathUtils.clamp(
            world.rotation.x + (e.key === 'ArrowUp' ? -0.1 : e.key === 'ArrowDown' ? 0.1 : 0),
            -0.7,
            0.7,
          );
        }
        draw();
      }
    };
    host.addEventListener('pointerdown', down);
    host.addEventListener('pointermove', move);
    host.addEventListener('pointerup', up);
    host.addEventListener('pointercancel', up);
    host.addEventListener('keydown', key);
    const observer = new ResizeObserver(resize);
    observer.observe(host);
    engine.current = { update };
    resize();
    update();
    return () => {
      observer.disconnect();
      engine.current = null;
      host.removeEventListener('pointerdown', down);
      host.removeEventListener('pointermove', move);
      host.removeEventListener('pointerup', up);
      host.removeEventListener('pointercancel', up);
      host.removeEventListener('keydown', key);
      scene.traverse((o) => {
        o.geometry?.dispose();
        if (o.material) {
          if (Array.isArray(o.material)) o.material.forEach((m) => m.dispose());
          else o.material.dispose();
        }
      });
      renderer.dispose();
      renderer.domElement.remove();
    };
  }, []);
  return (
    <div
      className={`globe-host ${hero ? 'hero-globe-host' : ''}`}
      ref={mount}
      role="img"
      aria-label={`Globo interattivo degli eventi ${year ?? '1970–2020'}. Trascina per ruotare oppure usa le frecce; Home ripristina la vista.`}
      tabIndex={0}
    >
      {failed && (
        <div className="globe-fallback">
          <span>◉</span>
          <p>
            La vista 3D richiede WebGL.
            <br />
            Esplora i dati con la timeline e i grafici qui sotto.
          </p>
        </div>
      )}
    </div>
  );
}
