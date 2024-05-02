class BaseController:
  def update(self, target_lataccel, current_lataccel, state):
    raise NotImplementedError

class OpenController(BaseController):
  def update(self, target_lataccel, current_lataccel, state):
    return target_lataccel

class SimpleController(BaseController):
  def update(self, target_lataccel, current_lataccel, state):
    return (target_lataccel - current_lataccel) * 0.3

class MambaController(BaseController):
  def __init__(self) -> None:
    self.prev_error = 0
    self.intergral_error = 0

    # controller gains
    self.kp = 0.5 # proportional gain
    self.ki = 0.1 # integral gain
    self.kd = 0.05 # derivative gain

  def update(self, target_lataccel, current_lataccel, state):
    error = target_lataccel - current_lataccel
    
    self.intergral_error += error
    
    derivative_error = error - self.prev_error
    
    self.prev_error = error

    if abs(error) > 0.1:
      self.kp *= 0.5
    else:
      self.kp *= 0.5

    steer_action = (self.kp * error) + (self.ki * self.intergral_error) + (self.kd * derivative_error)

    return steer_action
  
class AdaptivePIDController(BaseController):
  def __init__(self) -> None:
      self.prev_error = 0
      self.integral_error = 0

      # controller gains
      self.kp = 0.1  # proportional gain
      self.ki = 0.001  # integral gain
      self.kd = 0.00003  # derivative gain

      # adaptive gain
      self.kc = 0.01

  def update(self, target_lataccel, current_lataccel, state):
      error = target_lataccel - current_lataccel

      self.integral_error += error

      derivative_error = error - self.prev_error

      self.prev_error = error

      # adaptive control law
      self.kp = self.kp + self.kc * error * self.prev_error
      self.ki = self.ki + self.kc * error * self.integral_error
      # self.kd = self.kd + self.kc * error * derivative_error

      steer_action = (self.kp * error) + (self.ki * self.integral_error) + (self.kd * derivative_error)
      print(f"kp: {self.kp}, ki: {self.ki}, kd: {self.kd}, error: {error}")

      return steer_action
    
CONTROLLERS = {
  'open': OpenController,
  'simple': SimpleController,
  'mamba': MambaController,
  'adaptive_pid': AdaptivePIDController
}
