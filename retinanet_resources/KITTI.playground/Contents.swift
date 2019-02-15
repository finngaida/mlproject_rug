import Cocoa
import PlaygroundSupport

/* *
 Values Name Description
 0 type Describes the type of object: 'Car', 'Van', 'Truck',
 'Pedestrian', 'Person_sitting', 'Cyclist', 'Tram',
 'Misc' or 'DontCare'
 1 truncated Float from 0 (non-truncated) to 1 (truncated), where
 truncated refers to the object leaving image boundaries
 2 occluded Integer (0,1,2,3) indicating occlusion state:
    0 = fully visible, 1 = partly occluded
    2 = largely occluded, 3 = unknown
 3 alpha Observation angle of object, ranging [-pi..pi]
 [4-7] bbox 2D bounding box of object in the image (0-based index):
 contains left, top, right, bottom pixel coordinates
 [8-10] dimensions 3D object dimensions: height, width, length (in meters)
 [11-13] location 3D object location x,y,z in camera coordinates (in meters)
 14 rotation_y Rotation ry around Y-axis in camera coordinates [-pi..pi]
 15 score Only for results: Float, indicating confidence in
 detection, needed for p/r curves, higher is better.
 */
struct Observation {
    enum Format { case KITTI, RetinanetTrain, RetinanetOut }

    let name: String
    let `class`: String
    let rect: (x: Int, y: Int, x2: Int, y2: Int)

    // optional vars
    var certainty: Float? = nil
    var classificationTime: TimeInterval? = nil

    init?(name: String? = nil, _ rest: String, format: Format) {
        switch format {
        case .KITTI:
            let c = rest.components(separatedBy: " ")
            self.name = name!
            self.class = c[0]
            // ...

            guard let x = Float(c[4]), let y = Float(c[5]), let x2 = Float(c[6]), let y2 = Float(c[7]) else { return nil }
            self.rect = (x: Int(x), y: Int(y), x2: Int(x2), y2: Int(y2))

        case .RetinanetTrain:
            let c = rest.components(separatedBy: ",")
            guard c.count > 5 else { fatalError("Train Count: \(c.count)") }
            self.name = name ?? URL(fileURLWithPath: c[0]).lastPathComponent
            guard let x = Int(c[1]), let y = Int(c[2]), let x2 = Int(c[3]), let y2 = Int(c[4]) else { return nil }
            self.rect = (x: x, y: y, x2: x2, y2: y2)
            self.class = c[5]

        case .RetinanetOut:
            let c = rest.components(separatedBy: ",")
            guard c.count > 7 else { fatalError("Out Count too low: \(rest)") }
            self.name = name ?? URL(fileURLWithPath: c[0]).lastPathComponent
            guard let x = Int(c[1]), let y = Int(c[2]), let x2 = Int(c[3]), let y2 = Int(c[4]) else { return nil }
            self.rect = (x: x, y: y, x2: x2, y2: y2)
            self.class = c[5]
            self.certainty = Float(c[6])
            self.classificationTime = TimeInterval(c[7])
        }
    }

    func IoU(_ with: Observation) -> CGFloat {
        let myRect = CGRect(x: rect.x, y: rect.y, width: rect.x2-rect.x, height: rect.y2-rect.y)
        let theirRect = CGRect(x: with.rect.x, y: with.rect.y, width: with.rect.x2-with.rect.x, height: with.rect.y2-with.rect.y)

        let intersection = myRect.intersection(theirRect)
        let union = (myRect.width * myRect.height) + (theirRect.width * theirRect.height)
        return (intersection.width * intersection.height) / union
    }

    var tranformed: String {
//        return "/home/s3838730/data/ml/training/image_2/\(name).png,\(rect.x),\(rect.y),\(rect.x2),\(rect.y2),\(self.class)\n"
        return "/data/s3801128/training/image_2/\(name).png,\(rect.x),\(rect.y),\(rect.x2),\(rect.y2),\(self.class)\n"
    }
}

func bikes(in url: URL) throws -> [Observation] {
    let content = try String(contentsOf: url)
    let observations = content.components(separatedBy: "\n").dropLast()
    let bikes = observations.filter { s in
        let c = s.components(separatedBy: " ")
        guard let x = Float(c[4]), let y = Float(c[5]), let x2 = Float(c[6]), let y2 = Float(c[7]) else { return false }
        let isCyclist = c[0] == "Cyclist" // && (x2-x) * (y2-y) > 8000
        let isPedestrian = c[0] == "Pedestrian" // && (x2-x) * (y2-y) > 5000
        guard isCyclist || isPedestrian else { return false }
        return true
    }
    return bikes.compactMap { Observation(name: url.deletingPathExtension().lastPathComponent, $0, format: .KITTI) }
}

func createKITTICSVFile() {
    let base = playgroundSharedDataDirectory.appendingPathComponent("label_2")
    let fm = FileManager.default
    let limit = 10000
    var numBikes: Int = 0
    let writeURL = playgroundSharedDataDirectory.appendingPathComponent("out.csv")
    try? fm.removeItem(at: writeURL)
    fm.createFile(atPath: writeURL.path, contents: nil, attributes: nil)

    do {
        let urls = try fm.contentsOfDirectory(at: base, includingPropertiesForKeys: [], options: [])
        let handle = try FileHandle(forWritingTo: writeURL)

        outer: for url in urls {
            for bike in try bikes(in: url) {
                handle.write(bike.tranformed.data(using: .utf8)!)

                numBikes += 1
                if numBikes == limit {
                    break outer
                }
            }
        }
    } catch let e {
        print(e)
    }
}

func comparePredictions() {
    let inputString = try! String(contentsOf: Bundle.main.url(forResource: "kitti_bikes_only", withExtension: "csv")!)
    let predictionsString = try! String(contentsOf: Bundle.main.url(forResource: "predictions_pretrained", withExtension: "csv")!)

    let inputs = inputString.components(separatedBy: "\n").dropLast().compactMap { Observation($0, format: .RetinanetTrain) }
    let allPredictions: [Observation] = predictionsString.components(separatedBy: "\n").dropLast().compactMap { Observation($0, format: .RetinanetOut) }.filter { $0.class == "bicycle" }

    var errors: [String: [CGFloat]] = [:]

    var inputCursor = 0
    var predictionsCursor = 0
    while inputCursor < inputs.count {
        let currentExpectation = inputs[inputCursor]

        // get all expected predictions
        var expectations: [Observation] = [currentExpectation]
        inputCursor += 1

        while inputs.count > inputCursor && inputs[inputCursor].name == currentExpectation.name {
            expectations.append(inputs[inputCursor])
            inputCursor += 1
        }

        // get all predictions
        var predictions: [Observation] = []
        while allPredictions.count > predictionsCursor && allPredictions[predictionsCursor].name == currentExpectation.name {
            predictions.append(allPredictions[predictionsCursor])
            predictionsCursor += 1
        }

        // now compare
        // note: all inputs are cyclists, so it's enough to count bikes in the predictions for now, but this should obviously check the inputs class vs. the outputs'
        let expectedBikes = expectations.count
        let predictedBikes = predictions.count

        var ious = [CGFloat](repeating: 0, count: expectations.count)
        for i in 0..<expectations.count {
            for obs in predictions {
                let iou = expectations[i].IoU(obs)
                if iou > ious[i] {
                    ious[i] = iou
                }
            }
        }

        errors[currentExpectation.name] = ious
    }

    let meanIoU = errors.reduce(0, { $0 + $1.value.reduce(0, +) / CGFloat($1.value.count) }) / CGFloat(errors.count)
    let classificationTimes = allPredictions.compactMap({ $0.classificationTime })
    let meanCT = classificationTimes.reduce(0, +) / Double(classificationTimes.count)
    print("Mean IoU: \(meanIoU), mean CT: \(meanCT)")
}

//comparePredictions()
createKITTICSVFile()
