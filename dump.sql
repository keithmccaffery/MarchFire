


BEGIN
    CREATE TABLE doorfixes (
        fault_id INT,
        inspect NVARCHAR(MAX),
        fault NVARCHAR(MAX),
        remedy NVARCHAR(MAX)
    );
END



-- Insert statements...
INSERT INTO doorfixes VALUES('1','Inspect to determine if the fire-resistant doorset has been modified since the previous routine service','Door has been modified since previous routine service','Reinstate the door to previous as required');
INSERT INTO doorfixes VALUES('2','Inspect door leaves  are tagged in accordance with AS 1905.1','Door leaf does not have a fire rating tag','Ascertain that the door is fire rated door ');
INSERT INTO doorfixes VALUES('3','Inspect  door frames are tagged in accordance with AS 1905.1','Door leaf does not have a fire rating tag','Ascertain that  the door frame is fire rated');
INSERT INTO doorfixes VALUES('4','Inspect to ensure relevant statutory signage has been applied and that the location of the signage is in accordance with regulatory requirements','Statutory signage on door leaf is missing or incorrect','Supply the required signage (details to be provided)');
INSERT INTO doorfixes VALUES('5','Check that gaps between the edge of the door leaf and the door frame are in accordance with AS 1905.1 (not more than 3mm)','The gap from the door leaf edge to door frame is greater than 3mm','Install intumescent seals to achieve the required gap (<3mm)');
INSERT INTO doorfixes VALUES('6','Check that gaps between the bottom edge of the door and the floor level are in accordance with AS 1905.1 (not < 3mm and not >15mm)','The gap from the door leaf bottom to floor is more than 15mm or less than 3mm','Install door bottom upgrade kit to achieve the minimum gap (<15mm)');
INSERT INTO doorfixes VALUES('7','Inspect all the hardware required for suspension, closing and latching is fitted and is the make and model that has been tested for that door model','The door hardware is not appropriate for the make or model of door','Install the required hardware door (details to be provided)');
INSERT INTO doorfixes VALUES('8','Inspect all the hardware is located and securely attached and operational with correct fittings in accordance with AS 1905.1','Door hardware is not securely attached and/or does not operate correctly','Attach hardware appropriately and ensure correct operation');
INSERT INTO doorfixes VALUES('9','Verify the opening and closing forces are such that the doors can be easily opened and closed in normal conditions and in fire model','The door can not be opened or closed easily in normal conditions','Adjust door closer to allow easily opened or closed');
INSERT INTO doorfixes VALUES('10','Inspect the doorset is self-closing and self-latching if appropriate','The door is not self closing and/or self latching','Adjust door closer to achieve self closing and self latching');
INSERT INTO doorfixes VALUES('11','Where passage sets or knobs are incorporated inspect to see that the minimum 35mm to door stop is present','The passage sets and knobs do not have minimum 35mm clearance to door stop','####');
INSERT INTO doorfixes VALUES('12','Check closers are free from oil leaks','The door closer has oil leaks','Replace door closer');
INSERT INTO doorfixes VALUES('13','Inspect the door closer (body and arm) is free from obstruction by walls, fixtures and is operating freely throughout its swing','The door closer is obstructed and can not move freely through its swing','Install door closer so that it is not obstructed and can operate freely');
INSERT INTO doorfixes VALUES('14','Inspect any installed door seals are approved for use in the proprietary door type, functioning as intended and are not damaged','The door seals are damaged or may not be approved for this door model','Install the appropriate seals for the proprietary door');
INSERT INTO doorfixes VALUES('15','Check doors for any visible delamination, buckling, warping, bowing twisting or significant damage','The door is not free of buckling and/or warping and/or other damage','Install new fire rated door leaf');
INSERT INTO doorfixes VALUES('16','Check door edges are in good condition and free from any splitting or damage on all sides','The door edges are not in good condition and have signs of splitting','Install new door leaf or if appropriate repair ');
INSERT INTO doorfixes VALUES('17','Check door stop dimensions are approved for the proprietary door type and Fire Resistance Level','The door stops are not appropriate for proprietary door type','###');
INSERT INTO doorfixes VALUES('18','Check steel door frames are backfilled as required  for the proprietary door type and Fire Resistance Level','The steel door frames is not backfilled as required for fire door','Backfill the steel fire door frame ');
INSERT INTO doorfixes VALUES('19','Check door frame is free from excessive distortions at any point along the frame sections','The door frame has excessive distortions ','Replace steel door frame');
INSERT INTO doorfixes VALUES('20','Check to ensure doorframe incorporates a door stiker plate','The door frame does not have an incorporated striker plate','Install door frame strike plate');
INSERT INTO doorfixes VALUES('21','Check condition of frame','The door frame is generally of poor condition','Repair or replace door frame (depending on condtion of frame');
INSERT INTO doorfixes VALUES('22','Check proprietary door type is approved for use of a vision panel','The proprietary door type is not approved for a vision panel','Install an approved vision panel for the make and model of fire door');
INSERT INTO doorfixes VALUES('23','Check to ensure glass is approved for the proprietary door type, is in sound condition and free from cracks','The vision panel glass is not sound and/or is not free of cracks','Replace the vision panel glass');
INSERT INTO doorfixes VALUES('24','Check to ensure perimeter trim and framing are secure and in sound condition and all fixing srews are in placeand consistent with the fire test approvals for the proprietary door type','The vision panel frame is generally not sound and/or screws are missing','Install any missing screws in the vision panel');
INSERT INTO doorfixes VALUES('25','Check proprietary door type is approved for use with the fire-resistant air transfer grille and is installed as per the manufactures instructions','The proprietary door type is not approved for a air transfer grill','Install an approved air transfer grill for the make and model of fire door');
INSERT INTO doorfixes VALUES('26','Where required verify travel limiting device is installed with accordance with AS 1905.1','The travel limiting device is not installed with accordance with AS 1950.1','Install an approved travel limiting devicefor the make and model of fire door');
INSERT INTO doorfixes VALUES('27','Inspect the threshold for the door leaf is free from addition of any combustible covering since installed or previous inspection','The threshold of the door leaf is not free of any combustible covering','Remove the combustible material from the threshold of the door');
INSERT INTO doorfixes VALUES('28','Inspect the kickplates are securely fixed (where fitted)','The door kickplate is not securely fixed','Reaffix the kickplate ');
INSERT INTO doorfixes VALUES('29','Inspect to ensure that meeting stile astragals are correct for the proprietary door type is installed as per manufacture''s instructions, and are in good working order and incorporate seals where required','The meeting stile astragals are are not in good conditon ','Repair stile astragals ');
INSERT INTO doorfixes VALUES('30','Test that doors held in the open position,which require activation of detection system to close, to ensure the door closes satifactorily upon power failure or detector activation','The hold open function failed to operate as expected for power failure or detector ','Repair hold open function ');
INSERT INTO doorfixes VALUES('0','Door sound but want to record status and image','No fault','No remedy required');IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'doorfixes')

BEGIN
    CREATE TABLE em_lightfixes (
        fault_id INT,
        inspect NVARCHAR(MAX),
        fault NVARCHAR(MAX),
        remedy NVARCHAR(MAX)
    );
END



-- Insert statements...
INSERT INTO em_lightfixes VALUES(0,'Light sound but want to record status and image','No fault','No remedy');
INSERT INTO em_lightfixes VALUES(1,'Check there has not been interruption to mains power in last 16 hours','Mains power has been disrupted','Can not test emergency lighting in service duration');
INSERT INTO em_lightfixes VALUES(2,'Check directional beams for suitability','Directional beams shine into eyes','Adjust directional beams as required');
INSERT INTO em_lightfixes VALUES(3,'Check any fluorescent lamps for blackened ends','Fluorescent lamp has blackened ends','Fluorescent lamp has to be replaced');
INSERT INTO em_lightfixes VALUES(4,'Check emergency lighting operates in correct relationship with other lighting','Emergency lighting does not operates in correct relationship with other lighting','Make good emergency lighting to operate in correct relationship with other lighting');
INSERT INTO em_lightfixes VALUES(5,'Carry out in-service duration test by isolating emergency lighting from mains power','The light failed in-service duration test 90m minutes','Change the back up battery and redo the test after 16 hours of constant power');

BEGIN
    CREATE TABLE fireExfixes (
        fault_id INT,
        inspect NVARCHAR(MAX),
        fault NVARCHAR(MAX),
        remedy NVARCHAR(MAX)
    );
END



-- Insert statements...
INSERT INTO fireExfixes VALUES(0,'Fire extinguisher sound but want record status and image','No fault','No action required');
INSERT INTO fireExfixes VALUES(1,'The extinguisher should be conspicuous, readily accessible and in its assigned location as per your fire safety plan. Check that the location sign is at the correct height and is visible','Accessibility Signage Inadequate','Install accessibility signage');
INSERT INTO fireExfixes VALUES(2,'Ensure that the anti-tamper device is intact and positioned to serve its purpose','Anti-tamper seal faulty','Install anti-tamper seal ');
INSERT INTO fireExfixes VALUES(3,'Ensure that the extinguisher is clean and the operating instructions are legible','Exterior & instructions illegible','Replace fire extinguisher');
INSERT INTO fireExfixes VALUES(4,'Check that the maintenance record tag or label is securely attached by the required means and that the extinguisher has a unique means of identification.','Maintenance record label/tag missing','Replace missing maintenance record label/tag ');
INSERT INTO fireExfixes VALUES(5,'Check that the exterior surface and all attachments are not damaged and free of corrosion and is not pitted.','External damage','Replace fire extinguisher');
INSERT INTO fireExfixes VALUES(6,'Ensure that the hose & nozzle attachment are securely fitted, is free from obstruction and has no sign of damage or deterioration.','Outlet hose assembly faulty','Replace fire extinguisher');
INSERT INTO fireExfixes VALUES(7,'If a pressure indicator is fitted ensure that it is legible, registering with in the operating range and is operating correctly.','Pressure indicator faulty','Replace fire extinguisher');
INSERT INTO fireExfixes VALUES(8,'Check that the support bracket is appropriate, securely attached to a suitable structure and the fire extinguisher is easily removed','Support bracket faulty','Install suitable support bracket ');
INSERT INTO fireExfixes VALUES(9,'Weigh the extinguisher to determine that it is fully charged','Not fully charged','Replace fire extinguisher');
INSERT INTO fireExfixes VALUES(10,'Determine, where possible and without discharging any contents that the actuating device is free from damage and corrosion and moves freely.','Actuating device faulty','Replace fire extinguisher');
INSERT INTO fireExfixes VALUES(11,'Invert the extinguisher and ensure that the powder remains free flowing','Powder not free flowing','Replace fire extinguisher');
INSERT INTO fireExfixes VALUES(12,'Check that the extinguisher is not due for a hydrostatic test','Extinguisher due for hydrostatic test','Replace fire extinguisher');
INSERT INTO fireExfixes VALUES(13,'Determine, hat the internal discharge tube and strainer (where fitted) provide clear passage and are securely attached. "water & foam only (gas container type)"','Internal Components faulty','Replace fire extinguisher');

BEGIN
    CREATE TABLE results (
        id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT,
        asset NVARCHAR(MAX),
        fault_id INT,
        remedy NVARCHAR(MAX),
        comment NVARCHAR(MAX),
        image_url NVARCHAR(MAX),
        timestamp DATETIME
    );
END



-- Insert statements...

BEGIN
    CREATE TABLE images (
        id INT IDENTITY(56,1) PRIMARY KEY,
        result_id INT,
        image_url NVARCHAR(MAX),
        remedy NVARCHAR(MAX),
        FOREIGN KEY(result_id) REFERENCES results(id)
    );
END



-- Insert statements...


INSERT INTO images VALUES(56,192,'https://firstfire.blob.core.windows.net/firedoors1/image_1714561785692.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(57,193,'https://firstfire.blob.core.windows.net/firedoors1/image_1714562290589.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(58,193,'https://firstfire.blob.core.windows.net/firedoors1/image_1714562310192.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(59,194,'https://firstfire.blob.core.windows.net/firedoors1/image_1714564394373.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(60,194,'https://firstfire.blob.core.windows.net/firedoors1/image_1714564400447.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(61,194,'https://firstfire.blob.core.windows.net/firedoors1/image_1714564410091.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(62,195,'https://firstfire.blob.core.windows.net/firedoors1/image_1714564703270.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(63,195,'https://firstfire.blob.core.windows.net/firedoors1/image_1714564723715.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(64,196,'https://firstfire.blob.core.windows.net/firedoors1/image_1714736650496.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(65,196,'https://firstfire.blob.core.windows.net/firedoors1/image_1714736672665.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(66,197,'https://firstfire.blob.core.windows.net/firedoors1/image_1714736875915.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(67,197,'https://firstfire.blob.core.windows.net/firedoors1/image_1714736884695.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(68,198,'https://firstfire.blob.core.windows.net/firedoors1/image_1714896489728.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(69,198,'');
INSERT INTO images VALUES(70,199,'https://firstfire.blob.core.windows.net/firedoors1/image_1714896874378.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(71,200,'https://firstfire.blob.core.windows.net/firedoors1/image_1714897422138.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(72,201,'https://firstfire.blob.core.windows.net/firedoors1/image_1714967933556.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(73,201,'https://firstfire.blob.core.windows.net/firedoors1/image_1714967949883.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(74,202,'');
INSERT INTO images VALUES(75,203,'https://firstfire.blob.core.windows.net/firedoors1/image_1715045297308.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(76,204,'https://firstfire.blob.core.windows.net/firedoors1/image_1715081584563.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(77,205,'https://firstfire.blob.core.windows.net/firedoors1/image_1715081703534.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');
INSERT INTO images VALUES(78,205,'https://firstfire.blob.core.windows.net/firedoors1/image_1715081714168.jpg?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-05T14:08:47Z&st=2024-02-11T05:08:47Z&spr=https,http&sig=RXTEYfSJv1wwz9P6%2BrSJln8scy%2B15cRb8LBFDgWYPCY%3D');


BEGIN
    CREATE TABLE users (
        id INT IDENTITY(25,1) PRIMARY KEY,
        username NVARCHAR(255) NOT NULL,
        hash NVARCHAR(255),
        UNIQUE(username)
    );
END



-- Insert statements...

INSERT INTO users VALUES(25,'Tues1');
INSERT INTO users VALUES(26,'Tues2');
INSERT INTO users VALUES(27,'Td8');
INSERT INTO users VALUES(28,'Td9');

