let sketch3 = function(p){
  let worldWidth = 640
  let worldHeight = 400
  let worldAspect = (worldHeight/worldWidth);
  let hit = false;
  let watts = 0;
  let volts = 0;
  let currents = 0;
  let voltage = [,
    50,
    100,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500,
    550,
    600];

  let current = [390,
    390,
    370,
    200,
    150,
    150,
    145,
    145,
    141,
    140,
    120,
    0];

  p.setup = function() {
    let canvas = p.createCanvas(worldWidth, worldHeight);
    canvas.parent('mpptcalc2');
    p.collideDebug(false);
  }

  p.draw = function() {
    p.translate(0, p.height);
    p.scale(p.width / worldWidth, -p.height / worldHeight);
    p.background(255);
    
    let myDegrees = p.map(wMouseY(p.mouseY), 0, p.height, 0, 70);
    let v = p5.Vector.fromAngle(p.radians(myDegrees), 1000);
    let vx = v.x;
    let vy = v.y;
    
    let wp1 = p.createVector(voltage[0],current[0]);
    let wp2 = p.createVector(voltage[0],current[0]);
    
    for (let i=0; i<=voltage.length; i++){
      let p1 = p.createVector(voltage[i],current[i]);
      let p2 = p.createVector(voltage[i+1],current[i+1]);
      let p3 = p.createVector(0,0);
      let p4 = p.createVector(vx, vy);
      drawLines(wp1,wp2,p3,p4);
      wp1 = p1;
      wp2 = p2;
    }

    p.stroke('black');
    p.strokeWeight(6);
    p.line(0,0,600,0);
    p.line(0,0,0,400);
  }

  function drawLines(p1,p2,p3,p4){
    hit = p.collideLineLineVector(p1,p2,p3,p4, true);
    if(hit.x != false){
      p.stroke(255,0,0);
      p.fill(255,0,0);
      p.circle(hit.x, hit.y, 20);
      p.stroke(0,0,0);
      p.strokeWeight(2);
      p.fill(255,100,100,70);
      p.stroke(255,100,100);
      p.rect(0,0,hit.x,hit.y);
      p.push()
      p.scale(1,-1);
      p.textSize(32);
      volts = p.round(p.map(hit.x,0,500,0,30),1);
      currents = p.round(p.map(hit.y,0,300,0,5),1);
      watts = p.floor(volts*currents);
      p.stroke(0,0,0,255);
      p.text(watts + ' W', 450, -300);
      p.text(volts + ' V', 450, -250);
      p.text(currents + ' A', 450, -200);
      p.pop();
    }
    p.strokeWeight(5);
    p.stroke(0,0,255);
    p.line(p1.x, p1.y, p2.x, p2.y);
    p.stroke(240,200,0);
    p.strokeWeight(3);
    p.line(0, 0, p4.x, p4.y);
  }

  function wMouseX(pmouseX) {
    return pmouseX * (worldWidth / p.width)
  }

  function wMouseY(pmouseY) {
    return worldHeight - (pmouseY * (worldHeight / p.height))
  }
};

let p5sketch3 = new p5(sketch3);
