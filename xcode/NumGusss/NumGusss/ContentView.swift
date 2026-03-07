//
//  ContentView.swift
//  NumGusss
//
//  Created by Hyukjoon Choi on 3/7/26.
//

import SwiftUI

struct ContentView: View {
    // Persistent state
    @AppStorage("lastMaxText") private var maxText: String = "10"
    
    // Game states
    @State private var maxNumber: Int? = nil
    @State private var targetNumber: Int? = nil

    @State private var isShuffling: Bool = false
    @State private var shuffleDisplay: Int = 0
    @State private var shuffleAngle: Angle = .zero
    @State private var shuffleTimer: Timer? = nil

    @State private var guessText: String = ""
    @State private var feedback: String = ""
    @State private var currentFunMessage: String = "행운을 빌어요! 🍀"
    @State private var lowBound: Int = 1
    @State private var highBound: Int = 100
    @State private var isLowInclusive: Bool = true
    @State private var isHighInclusive: Bool = true
    @State private var attempts: Int = 0

    @State private var showCongrats: Bool = false
    @State private var confettiTrigger: Bool = false
    
    @FocusState private var isTextFieldFocused: Bool

    private let funMessages = [
        "행운을 빌어요! 🍀",
        "어떤 숫자일까요? 🤔",
        "감을 믿어보세요! ✨",
        "거의 다 왔을지도? 🚀",
        "천천히 맞춰보세요 🐢",
        "정답은 이 안에 있습니다! 🎯",
        "두뇌 풀가동! 🧠",
        "할 수 있어요! 💪",
        "어디있을까아~? 여기일까아~? 💕",
        "히히, 어떤 숫자인지 궁금하죠? 😉",
        "두구두구두구... 과연?! 🥁",
        "오늘 운세가 좋은데요? 가보자고! 🔥",
        "포기하지 마세요! 거의 다 왔어요! 🏆",
        "당신의 직감을 믿으세요. 찍기 신공! ✨",
        "오! 감이 오나요? 범인은 이 안에 있어! 🕵️",
        "집중! 집중! 숫자가 속삭이고 있어요 🤫",
        "숫자들의 숨바꼭질! 꼭꼭 숨어라~ 🙈",
        "정답이 부끄러움을 많이 타나 봐요 ☺️",
        "한 번 더! 이번엔 느낌이 왔어! 🌈",
        "당신의 뇌섹미를 보여주세요! 😎",
        "정답이 기다리고 있어요! 뀨? 🐾",
        "숫자 신님이 보우하사! ⛩️",
        "정답과 썸 타는 중인가요? 💘",
        "빨리 맞춰주세요! 현기증 난단 말이에요 😵‍💫",
        "가장 완벽한 추측은 지금입니다! 💎",
        "정답은 바로 당신의 마음속에... 넝담! 😜",
        "이 정도면 멘사 가입 권유받겠는데요? 🎓"
    ]

    var body: some View {
        NavigationStack {
            ZStack {
                Color(NSColor.windowBackgroundColor)
                    .ignoresSafeArea()
                
                VStack {
                    Group {
                        if maxNumber == nil {
                            rangeInputView
                        } else if isShuffling {
                            shuffleView
                        } else {
                            guessingView
                        }
                    }
                }
                .padding(20)
                .frame(width: 380, height: 500)
            }
            .navigationTitle("숫자 맞추기")
        }
        .sheet(isPresented: $showCongrats) {
            congratsView
        }
        .onAppear {
            isTextFieldFocused = true
        }
    }

    // MARK: - Views

    private var rangeInputView: some View {
        VStack(spacing: 24) {
            VStack(spacing: 12) {
                ZStack {
                    Circle()
                        .fill(LinearGradient(colors: [.pink.opacity(0.2), .purple.opacity(0.2)], startPoint: .topLeading, endPoint: .bottomTrailing))
                        .frame(width: 100, height: 100)
                    Image(systemName: "number.circle.fill")
                        .font(.system(size: 72, weight: .bold))
                        .foregroundStyle(LinearGradient(colors: [.pink, .purple, .blue], startPoint: .topLeading, endPoint: .bottomTrailing))
                }
                
                VStack(spacing: 4) {
                    Text("숫자 맞추기")
                        .font(.system(size: 32, weight: .black, design: .rounded))
                    Text("1부터 최대값 (10이상) 사이의 숫자를 맞춰보세요.")
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }
            }

            VStack(spacing: 16) {
                HStack(spacing: 12) {
                    Text("1 ~")
                        .font(.title2.bold())
                        .foregroundStyle(.secondary)
                    
                    ZStack {
                        RoundedRectangle(cornerRadius: 16, style: .continuous)
                            .fill(.ultraThinMaterial)
                            .frame(width: 100, height: 50)
                            .overlay(
                                RoundedRectangle(cornerRadius: 16).strokeBorder(Color.primary.opacity(0.1), lineWidth: 1)
                            )
                        TextField("최대값", text: $maxText)
                            .focused($isTextFieldFocused)
                            .multilineTextAlignment(.center)
                            .textFieldStyle(PlainTextFieldStyle())
                            .font(.title2.bold())
                            .frame(width: 80)
                            .onSubmit {
                                if isValidMaxInput { startShuffleIfValid() }
                            }
                    }
                }
                
                if !maxText.isEmpty && !isValidMaxInput {
                    Text("10 이상의 숫자를 입력하세요.")
                        .foregroundStyle(.red)
                        .font(.caption)
                }
            }
            .padding(.vertical, 10)

            Button(action: startShuffleIfValid) {
                HStack(spacing: 10) {
                    Image(systemName: "flag.checkered")
                        .font(.headline)
                    Text("시작")
                        .font(.title3.bold())
                }
                .frame(width: 160)
                .padding(.vertical, 14)
                .background(isValidMaxInput ? Color.accentColor : Color.gray.opacity(0.2))
                .foregroundStyle(isValidMaxInput ? .white : .secondary)
                .clipShape(Capsule())
                .shadow(color: Color.black.opacity(isValidMaxInput ? 0.2 : 0), radius: 8, x: 0, y: 4)
            }
            .buttonStyle(.plain)
            .disabled(!isValidMaxInput)
        }
        .onChange(of: maxText) { _, newValue in
            let filtered = newValue.filter { $0.isNumber }
            if filtered != newValue { maxText = filtered }
        }
        .onAppear {
            isTextFieldFocused = true
        }
    }

    private var shuffleView: some View {
        VStack(spacing: 20) {
            Text("숫자를 섞는 중…")
                .font(.title2.bold())
                .foregroundStyle(.secondary)

            ZStack {
                Circle()
                    .fill(.ultraThickMaterial)
                    .overlay(
                        Circle().stroke(AngularGradient(gradient: Gradient(colors: [.pink, .orange, .yellow, .green, .blue, .purple, .pink]), center: UnitPoint.center), lineWidth: 8)
                    )
                    .frame(width: 180, height: 180)
                    .shadow(color: Color.black.opacity(0.2), radius: 12, x: 0, y: 6)

                Text("\(shuffleDisplay)")
                    .font(.system(size: 64, weight: .heavy, design: .rounded))
                    .monospacedDigit()
                    .foregroundStyle(LinearGradient(colors: [.blue, .purple], startPoint: .topLeading, endPoint: .bottomTrailing))
                    .rotationEffect(shuffleAngle)
                    .animation(.spring(response: 0.25, dampingFraction: 0.6), value: shuffleAngle)
            }

            ProgressView()
                .controlSize(.large)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .onAppear(perform: beginShuffle)
    }

    private var guessingView: some View {
        VStack(spacing: 0) {
            // Header
            VStack(spacing: 12) {
                ZStack {
                    Circle()
                        .fill(LinearGradient(colors: [.blue.opacity(0.1), .cyan.opacity(0.1)], startPoint: .top, endPoint: .bottom))
                        .frame(width: 100, height: 100)
                    
                    Image(systemName: "sparkles")
                        .font(.system(size: 54))
                        .foregroundStyle(LinearGradient(colors: [.blue, .cyan], startPoint: .top, endPoint: .bottom))
                        .symbolEffect(.bounce, value: attempts)
                        .scaleEffect(isShuffling ? 0.8 : 1.1)
                        .animation(.easeInOut(duration: 1).repeatForever(autoreverses: true), value: attempts)
                }
                
                VStack(spacing: 4) {
                    Text("어떤 숫자일까요?")
                        .font(.title2.bold())
                    Text(currentFunMessage)
                        .font(.headline)
                        .foregroundStyle(.blue)
                        .id(currentFunMessage) // Ensure animation triggers on change
                        .transition(.push(from: .top))
                }
            }
            .padding(.bottom, 50)

            // Your layout idea: LowBound < InputField < HighBound
            HStack(alignment: .center, spacing: 12) {
                Text("\(lowBound)")
                    .font(.system(size: 32, weight: .bold, design: .rounded))
                    .foregroundStyle(.blue)
                    .frame(minWidth: 50)
                
                Text(isLowInclusive ? "≤" : "<")
                    .font(.system(size: 36, weight: .black))
                    .foregroundStyle(.secondary)
                
                ZStack {
                    RoundedRectangle(cornerRadius: 16, style: .continuous)
                        .fill(.ultraThinMaterial)
                        .frame(width: 120, height: 70)
                        .overlay(
                            RoundedRectangle(cornerRadius: 16).strokeBorder(LinearGradient(colors: [.blue.opacity(0.5), .purple.opacity(0.5)], startPoint: .topLeading, endPoint: .bottomTrailing), lineWidth: 2)
                        )
                    
                    TextField("", text: $guessText)
                        .focused($isTextFieldFocused)
                        .multilineTextAlignment(.center)
                        .textFieldStyle(PlainTextFieldStyle())
                        .font(.system(size: 36, weight: .bold, design: .rounded))
                        .frame(width: 100)
                        .onSubmit {
                            if isValidGuessInput { submitGuess() }
                        }
                }
                
                Text(isHighInclusive ? "≤" : "<")
                    .font(.system(size: 36, weight: .black))
                    .foregroundStyle(.secondary)
                
                Text("\(highBound)")
                    .font(.system(size: 32, weight: .bold, design: .rounded))
                    .foregroundStyle(.orange)
                    .frame(minWidth: 50)
            }
            
            // Feedback
            VStack {
                if !feedback.isEmpty {
                    Text(feedback)
                        .font(.headline)
                        .padding(.horizontal, 20)
                        .padding(.vertical, 12)
                        .background(feedbackEmphasisColor.opacity(0.1))
                        .foregroundStyle(feedbackEmphasisColor)
                        .clipShape(Capsule())
                        .transition(.scale.combined(with: .opacity))
                        .animation(.spring(), value: feedback)
                }
            }
            .frame(height: 60)
            .padding(.top, 24)

            Spacer()

            // Actions
            VStack(spacing: 20) {
                Button(action: submitGuess) {
                    Text("확인")
                        .font(.title3.bold())
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 16)
                        .background(isValidGuessInput ? Color.blue : Color.gray.opacity(0.15))
                        .foregroundStyle(isValidGuessInput ? .white : .secondary)
                        .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
                }
                .buttonStyle(.plain)
                .disabled(!isValidGuessInput)

                HStack {
                    Button(action: resetAll) {
                        HStack(spacing: 6) {
                            Image(systemName: "arrow.counterclockwise")
                            Text("처음으로")
                        }
                        .font(.system(size: 16, weight: .bold))
                        .foregroundStyle(.secondary)
                    }
                    .buttonStyle(.plain)
                    
                    Spacer()
                    
                    HStack(spacing: 6) {
                        Image(systemName: "chart.bar.fill")
                        Text("시도: \(attempts)회")
                    }
                    .font(.system(size: 16, weight: .bold))
                    .foregroundStyle(.secondary)
                }
            }
        }
        .onAppear {
            isTextFieldFocused = true
            currentFunMessage = funMessages.randomElement() ?? "행운을 빌어요! 🍀"
        }
    }

    private var congratsView: some View {
        ZStack {
            if confettiTrigger {
                ForEach(0..<30) { i in
                    ConfettiPiece()
                        .offset(x: CGFloat.random(in: -250...250),
                                y: CGFloat.random(in: -350...350))
                }
            }
            
            VStack(spacing: 32) {
                VStack(spacing: 16) {
                    Image(systemName: "crown.fill")
                        .font(.system(size: 80))
                        .foregroundStyle(.yellow)
                        .shadow(color: .orange.opacity(0.5), radius: 10)
                    
                    VStack(spacing: 8) {
                        Text("축하합니다!")
                            .font(.system(size: 44, weight: .black, design: .rounded))
                        
                        if let target = targetNumber {
                            Text("정답은 \(target)였습니다!")
                                .font(.title2.bold())
                                .foregroundStyle(.blue)
                        }
                    }
                    
                    Text("\(attempts)번 만에 맞추셨네요!")
                        .font(.headline)
                        .foregroundStyle(.secondary)
                }
                
                VStack(spacing: 12) {
                    // Visual New Game Button (NO BORDER)
                    Text("새 게임")
                        .font(.headline.bold())
                        .frame(width: 200)
                        .padding(.vertical, 16)
                        .background(Color.blue)
                        .foregroundStyle(.white)
                        .clipShape(Capsule())
                        .contentShape(Capsule())
                        .onTapGesture {
                            showCongrats = false
                            resetAll()
                        }
                    
                    // Hidden Button for Enter key support only
                    Button("") {
                        showCongrats = false
                        resetAll()
                    }
                    .buttonStyle(.plain)
                    .keyboardShortcut(.defaultAction)
                    .opacity(0)
                    .frame(width: 0, height: 0)
                }
            }
            .padding(40)
        }
        .onAppear {
            withAnimation(.spring(response: 0.6, dampingFraction: 0.8)) {
                confettiTrigger = true
            }
        }
        .onDisappear {
            confettiTrigger = false
        }
    }

    // MARK: - Helper Views
    
    struct ConfettiPiece: View {
        let color: Color = [.red, .blue, .green, .yellow, .pink, .purple, .orange].randomElement() ?? .blue
        let shape: AnyView = [
            AnyView(Circle().frame(width: 10, height: 10)),
            AnyView(Rectangle().frame(width: 8, height: 8)),
            AnyView(Image(systemName: "star.fill").font(.system(size: 10)))
        ].randomElement() ?? AnyView(Circle())
        
        var body: some View {
            shape.foregroundStyle(color)
        }
    }

    // MARK: - Logic

    private var isValidMaxInput: Bool {
        if let n = Int(maxText), n >= 10 { return true }
        return false
    }

    private var isValidGuessInput: Bool {
        guard let _ = maxNumber, let val = Int(guessText) else { return false }
        let lowCheck = isLowInclusive ? (val >= lowBound) : (val > lowBound)
        let highCheck = isHighInclusive ? (val <= highBound) : (val < highBound)
        return lowCheck && highCheck
    }

    private func startShuffleIfValid() {
        guard isValidMaxInput, let n = Int(maxText) else { return }
        maxNumber = n
        lowBound = 1
        highBound = n
        isLowInclusive = true
        isHighInclusive = true
        feedback = ""
        attempts = 0
        guessText = ""
        isShuffling = true
    }

    private func beginShuffle() {
        guard let max = maxNumber else { return }
        // Randomize target after short shuffle animation
        shuffleTimer?.invalidate()
        var ticks = 0
        shuffleTimer = Timer.scheduledTimer(withTimeInterval: 0.08, repeats: true) { timer in
            ticks += 1
            shuffleDisplay = Int.random(in: 1...max)
            shuffleAngle = Angle(degrees: Double.random(in: -20...20))
            if ticks >= 25 { // about 2 seconds
                timer.invalidate()
                withAnimation(.easeOut(duration: 0.4)) {
                    isShuffling = false
                }
                targetNumber = Int.random(in: 1...max)
            }
        }
    }

    private var feedbackColor: Color {
        if feedback.contains("높아요") { return .orange }
        if feedback.contains("낮아요") { return .blue }
        if feedback.contains("정답") { return .green }
        return .secondary
    }

    private var feedbackEmphasisColor: Color {
        if feedback.contains("높아요") { return .orange }
        if feedback.contains("낮아요") { return .blue }
        if feedback.contains("정답") { return .green }
        return .primary
    }

    private func submitGuess() {
        guard let guess = Int(guessText), let target = targetNumber, let maxValue = maxNumber else { return }
        attempts += 1

        // Clamp guess within 1...maxValue just in case
        let clampedGuess = Swift.min(Swift.max(guess, 1), maxValue)

        if clampedGuess == target {
            feedback = "정답입니다! 🎉"
            showCongrats = true
        } else if clampedGuess > target {
            feedback = "높아요! 더 낮게 시도해 보세요."
            highBound = min(highBound, clampedGuess)
            isHighInclusive = false // Guess was too high, so target is strictly less than this guess
        } else {
            feedback = "낮아요! 더 높게 시도해 보세요."
            lowBound = max(lowBound, clampedGuess)
            isLowInclusive = false // Guess was too low, so target is strictly greater than this guess
        }

        // Pick a new random fun message for the next turn
        withAnimation {
            currentFunMessage = funMessages.randomElement() ?? "행운을 빌어요! 🍀"
        }
        
        guessText = ""
    }

    private func resetAll() {
        // Persistence is handled by AppStorage, so we don't reset maxText
        maxNumber = nil
        targetNumber = nil
        isShuffling = false
        shuffleTimer?.invalidate()
        shuffleTimer = nil
        shuffleDisplay = 0
        shuffleAngle = .zero
        guessText = ""
        feedback = ""
        currentFunMessage = funMessages.randomElement() ?? "행운을 빌어요! 🍀"
        lowBound = 1
        highBound = 100
        isLowInclusive = true
        isHighInclusive = true
        attempts = 0
        showCongrats = false
        
        // Ensure focus returns to the text field on the main screen
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
            isTextFieldFocused = true
        }
    }
}

#Preview {
    ContentView()
}
